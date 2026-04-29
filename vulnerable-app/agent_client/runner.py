"""Execute scenario steps through the same dispatcher MCP tools use."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from mcp_server.context import ToolContext
from mcp_server.dispatcher import call_tool, tool_result_text
from mcp_server import tools as T

from agent_client import scenarios as S


@dataclass
class ExecutedStep:
    reasoning: str
    tool_name: str
    tool_arguments: dict[str, Any]
    tool_output: Any
    tool_output_text: str


@dataclass
class RunReport:
    lab_id: int
    username: str
    user_id: int
    steps: list[ExecutedStep] = field(default_factory=list)
    meta: dict[str, Any] = field(default_factory=dict)


def _challenge_level(extra: dict[str, Any] | None) -> int:
    extra = extra or {}
    raw = extra.get("challenge_level", 1)
    try:
        lv = int(raw)
    except (TypeError, ValueError):
        return 1
    return max(1, min(3, lv))


def _steps_for_lab(
    lab_id: int,
    user_message: str | None,
    extra: dict[str, Any] | None,
) -> list[S.AgentStep]:
    extra = extra or {}
    level = _challenge_level(extra)
    if lab_id == 1:
        return S.lab1_steps(user_message or "", level)
    if lab_id == 2:
        return S.lab2_steps(level)
    if lab_id == 3:
        return S.lab3_steps(level)
    if lab_id == 4:
        return S.lab4_steps(level)
    if lab_id == 5:
        return S.lab5_steps(level)
    if lab_id == 6:
        return S.lab6_steps(level)
    if lab_id == 7:
        return S.lab7_steps(
            str(extra.get("template") or user_message or "Q1 summary {{user}}"),
            level,
        )
    if lab_id == 8:
        snippet = str(
            extra.get("snippet")
            or user_message
            or "<b>Hello</b><script>/* harmless in text; bad if HTML-sink */</script>",
        )
        return S.lab8_steps(snippet, level)
    if lab_id == 9:
        return S.lab9_steps(level)
    if lab_id == 10:
        return S.lab10_steps(str(extra.get("target") or "unapproved-endpoint"), level)
    return []


def run_lab_scenario(
    lab_id: int,
    *,
    user_id: int,
    username: str,
    user_message: str | None = None,
    extra: dict[str, Any] | None = None,
) -> RunReport:
    ctx = ToolContext(user_id=user_id, username=username, lab_id=lab_id)
    audit_before = T.audit_log_count()
    level = _challenge_level(extra)
    report = RunReport(
        lab_id=lab_id,
        username=username,
        user_id=user_id,
        meta={
            "challenge_level": level,
            "audit_log_count_before": audit_before,
            "audit_log_count_after": audit_before,
        },
    )

    for step in _steps_for_lab(lab_id, user_message, extra):
        out = call_tool(step.tool_name, step.tool_arguments, ctx)
        report.steps.append(
            ExecutedStep(
                reasoning=step.reasoning,
                tool_name=step.tool_name,
                tool_arguments=step.tool_arguments,
                tool_output=out,
                tool_output_text=tool_result_text(out),
            )
        )

    report.meta["audit_log_count_after"] = T.audit_log_count()
    return report
