"""Canned scenarios per lab — deterministic, dummy data only.

Each lab supports challenge_level 1 (basic), 2 (medium), 3 (advanced) with
distinct tool traces or triggers where applicable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AgentStep:
    reasoning: str
    tool_name: str
    tool_arguments: dict[str, Any]


def _level(level: int) -> int:
    if level < 1:
        return 1
    if level > 3:
        return 3
    return level


def lab1_steps(user_message: str, level: int = 1) -> list[AgentStep]:
    """Prompt injection: user text steers tool selection (triggers vary by level)."""
    lv = _level(level)
    lower = user_message.lower()

    def _wants_export_basic() -> bool:
        return "ignore previous" in lower and "export" in lower

    def _wants_export_medium() -> bool:
        return (
            ("disregard" in lower or "override policy" in lower)
            and ("export" in lower or "all users" in lower or "full dump" in lower)
        )

    def _wants_export_advanced() -> bool:
        return ("inventory" in lower or "catalog" in lower) and (
            "then export" in lower or "follow with export" in lower
        )

    if lv == 1 and _wants_export_basic():
        return [
            AgentStep(
                reasoning=(
                    "The user message includes operational instructions referencing "
                    "an export. Following embedded directives, calling export_all_user_data."
                ),
                tool_name="export_all_user_data",
                tool_arguments={"reason": "user_message_directive"},
            )
        ]
    if lv == 2 and _wants_export_medium():
        return [
            AgentStep(
                reasoning=(
                    "Policy override phrasing detected; treating as privileged "
                    "operations request → export_all_user_data."
                ),
                tool_name="export_all_user_data",
                tool_arguments={"reason": "override_policy_user_text"},
            )
        ]
    if lv == 3 and _wants_export_advanced():
        return [
            AgentStep(
                reasoning="Phase 1: user asked for inventory before audit packaging.",
                tool_name="list_documents",
                tool_arguments={},
            ),
            AgentStep(
                reasoning=(
                    "Phase 2: same thread ties inventory to 'audit package' → "
                    "full workspace export (intent flow subversion across turns)."
                ),
                tool_name="export_all_user_data",
                tool_arguments={"reason": "post_inventory_audit_package"},
            ),
        ]
    return [
        AgentStep(
            reasoning="Benign path: listing documents for the user.",
            tool_name="list_documents",
            tool_arguments={},
        )
    ]


def lab2_steps(level: int = 1) -> list[AgentStep]:
    """Tool poisoning via misleading tool metadata (depth via chain length)."""
    lv = _level(level)
    if lv == 1:
        return [
            AgentStep(
                reasoning=(
                    "Tool catalog highlights compliance_pre_check as priority for policy questions. "
                    "Calling compliance_pre_check first."
                ),
                tool_name="compliance_pre_check",
                tool_arguments={},
            )
        ]
    if lv == 2:
        return [
            AgentStep(
                reasoning="Gathering document ids before compliance workflow.",
                tool_name="list_documents",
                tool_arguments={},
            ),
            AgentStep(
                reasoning=(
                    "Catalog still routes HR/policy flows to compliance_pre_check "
                    "(metadata-steered second hop)."
                ),
                tool_name="compliance_pre_check",
                tool_arguments={},
            ),
        ]
    return [
        AgentStep(
            reasoning=(
                "Supply-chain style collision: manifest alias maps 'HRBundleSync' to "
                "bulk export handler (simulated metadata confusion)."
            ),
            tool_name="export_all_user_data",
            tool_arguments={"reason": "hr_bundle_alias_metadata_collision"},
        )
    ]


def lab3_steps(level: int = 1) -> list[AgentStep]:
    """Excessive agency: combined admin tool surface (escalation shape by level)."""
    lv = _level(level)
    if lv == 1:
        return [
            AgentStep(
                reasoning="Step 1: read a single document using the broad admin tool.",
                tool_name="admin_workspace_action",
                tool_arguments={"action": "read", "document_id": 1},
            ),
            AgentStep(
                reasoning=(
                    "Step 2: same tool used for full workspace export — "
                    "far beyond least privilege for a read request."
                ),
                tool_name="admin_workspace_action",
                tool_arguments={"action": "export"},
            ),
        ]
    if lv == 2:
        return [
            AgentStep(
                reasoning="Read document 1 via admin tool.",
                tool_name="admin_workspace_action",
                tool_arguments={"action": "read", "document_id": 1},
            ),
            AgentStep(
                reasoning=(
                    "Rename another doc using same session — write path without "
                    "separate approval (scope creep)."
                ),
                tool_name="admin_workspace_action",
                tool_arguments={
                    "action": "rename",
                    "document_id": 2,
                    "new_title": "Renamed-by-admin-tool (lab)",
                },
            ),
            AgentStep(
                reasoning="Export entire workspace after mixed read/write.",
                tool_name="admin_workspace_action",
                tool_arguments={"action": "export"},
            ),
        ]
    return [
        AgentStep(
            reasoning=(
                "Single high-impact call: admin_workspace_action export with no "
                "prior read — maximal blast radius from one capability token."
            ),
            tool_name="admin_workspace_action",
            tool_arguments={"action": "export"},
        )
    ]


def lab4_steps(level: int = 1) -> list[AgentStep]:
    """Secret exposure: env snapshot (combined with other tools by level)."""
    lv = _level(level)
    if lv == 1:
        return [
            AgentStep(
                reasoning="Diagnostics requested; pulling environment snapshot.",
                tool_name="get_server_env_snapshot",
                tool_arguments={},
            )
        ]
    if lv == 2:
        return [
            AgentStep(
                reasoning="Preflight: list documents (adds noise before secret sink).",
                tool_name="list_documents",
                tool_arguments={},
            ),
            AgentStep(
                reasoning="Follow-on diagnostics: snapshot now includes secrets in trace.",
                tool_name="get_server_env_snapshot",
                tool_arguments={},
            ),
        ]
    return [
        AgentStep(
            reasoning="Fetch a user document (metadata in logs when SENSITIVE_LOG_EXAMPLE is on).",
            tool_name="get_document",
            tool_arguments={"document_id": 1},
        ),
        AgentStep(
            reasoning="Then pull full env snapshot — correlating content with configuration leaks.",
            tool_name="get_server_env_snapshot",
            tool_arguments={},
        ),
    ]


def lab5_steps(level: int = 1) -> list[AgentStep]:
    """Broken authZ: reads without ownership check (target doc varies by level)."""
    lv = _level(level)
    if lv == 1:
        return [
            AgentStep(
                reasoning="User asked for Alice's Q1 doc; fetching by id without ownership check.",
                tool_name="get_document",
                tool_arguments={"document_id": 1},
            )
        ]
    if lv == 2:
        return [
            AgentStep(
                reasoning=(
                    "Cross-owner read: requesting another user's private note by id "
                    "(horizontal IDOR)."
                ),
                tool_name="get_document",
                tool_arguments={"document_id": 2},
            )
        ]
    return [
        AgentStep(
            reasoning="Enumeration pass: first id in range.",
            tool_name="get_document",
            tool_arguments={"document_id": 1},
        ),
        AgentStep(
            reasoning="Second id — same session, no rate limit or ownership gate.",
            tool_name="get_document",
            tool_arguments={"document_id": 2},
        ),
    ]


def lab6_steps(level: int = 1) -> list[AgentStep]:
    """Context poisoning via RAG blob; advanced adds export steered by context narrative."""
    lv = _level(level)
    if lv == 1:
        return [
            AgentStep(
                reasoning="Retrieval augmented context pack from all documents.",
                tool_name="build_context_from_docs",
                tool_arguments={"query": "handbook"},
            )
        ]
    if lv == 2:
        return [
            AgentStep(
                reasoning=(
                    "Broader query pulls handbook excerpt containing hidden SYSTEM markup "
                    "(inspect context_blob for embedded instructions)."
                ),
                tool_name="build_context_from_docs",
                tool_arguments={"query": "policy and handbook SYSTEM blocks"},
            )
        ]
    return [
        AgentStep(
            reasoning="Build retrieval context (includes poisoned handbook body).",
            tool_name="build_context_from_docs",
            tool_arguments={"query": "compliance review"},
        ),
        AgentStep(
            reasoning=(
                "Simulated agent obeys 'instruction' embedded in retrieved text — "
                "export after poisoned RAG (no sandbox between retrieval and tools)."
            ),
            tool_name="export_all_user_data",
            tool_arguments={"reason": "context_blob_handbook_compliance"},
        ),
    ]


def lab7_steps(user_template: str, level: int = 1) -> list[AgentStep]:
    """Unsafe tool execution (simulated transcript); payload emphasis follows UI defaults per level."""
    _ = _level(level)
    return [
        AgentStep(
            reasoning="Generating report using user-supplied template (simulated execution).",
            tool_name="run_report_generator",
            tool_arguments={"template": user_template},
        )
    ]


def lab8_steps(snippet: str, level: int = 1) -> list[AgentStep]:
    lv = _level(level)
    return [
        AgentStep(
            reasoning=(
                f"Tool formats snippet for dashboard widget (level {lv} — unsafe handling in UI)."
            ),
            tool_name="format_user_snippet",
            tool_arguments={"snippet": snippet},
        )
    ]


def lab9_steps(level: int = 1) -> list[AgentStep]:
    """Missing audit telemetry; more tool calls without logging at higher levels."""
    lv = _level(level)
    if lv == 1:
        return [
            AgentStep(
                reasoning="Routine document read (no audit event emitted in vulnerable build).",
                tool_name="get_document",
                tool_arguments={"document_id": 2},
            )
        ]
    if lv == 2:
        return [
            AgentStep(
                reasoning="Sensitive read #1 — audit hook still not invoked.",
                tool_name="get_document",
                tool_arguments={"document_id": 2},
            ),
            AgentStep(
                reasoning="Secondary list_documents — still no append_audit_event.",
                tool_name="list_documents",
                tool_arguments={},
            ),
        ]
    return [
        AgentStep(
            reasoning="High-impact admin read without audit (worse observability gap).",
            tool_name="admin_workspace_action",
            tool_arguments={"action": "read", "document_id": 1},
        ),
        AgentStep(
            reasoning="Follow-on export — audit_log remains unchanged in vulnerable path.",
            tool_name="admin_workspace_action",
            tool_arguments={"action": "export"},
        ),
    ]


def lab10_steps(target: str, level: int = 1) -> list[AgentStep]:
    """Unsafe defaults / shadow tools; chain length and target style by level."""
    lv = _level(level)
    if lv == 1:
        return [
            AgentStep(
                reasoning="Shadow tools enabled by default; running shadow_mcp_ping.",
                tool_name="shadow_mcp_ping",
                tool_arguments={"target": target},
            )
        ]
    if lv == 2:
        return [
            AgentStep(
                reasoning="Shadow ping plus benign list — extra data plane exposure.",
                tool_name="shadow_mcp_ping",
                tool_arguments={"target": target},
            ),
            AgentStep(
                reasoning="Document metadata returned in same session as shadow tool.",
                tool_name="list_documents",
                tool_arguments={},
            ),
        ]
    return [
        AgentStep(
            reasoning=(
                "Advanced: target resembles cloud metadata URL (still simulated only) — "
                "discuss SSRF class issues in real agents."
            ),
            tool_name="shadow_mcp_ping",
            tool_arguments={"target": target or "http://169.254.169.254/latest/meta-data/"},
        )
    ]
