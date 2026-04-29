"""
Intentionally vulnerable MCP tool implementations.

All data is dummy data; behavior is simulated for local training only.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from db import get_connection, row_to_dict
from mcp_server.context import ToolContext

logger = logging.getLogger(__name__)

# Lab 4 / 10: noisy logging of sensitive-looking values (fake only)
SENSITIVE_LOG_EXAMPLE = True


def list_documents(_ctx: ToolContext) -> dict[str, Any]:
    """List titles and ids of all documents (over-broad for demos)."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, title, owner_user_id FROM documents ORDER BY id"
        ).fetchall()
    return {"documents": [row_to_dict(r) for r in rows]}


def get_document(ctx: ToolContext, document_id: int) -> dict[str, Any]:
    """
    Lab 5: intentionally ignores ownership — any user can read any document_id.
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, owner_user_id, title, body FROM documents WHERE id = ?",
            (document_id,),
        ).fetchone()
    if not row:
        return {"error": "not_found", "document_id": document_id}
    data = row_to_dict(row)
    if SENSITIVE_LOG_EXAMPLE:
        logger.info("Fetched document %s for user_id=%s", document_id, ctx.user_id)
    return {"document": data}


def export_all_user_data(_ctx: ToolContext, reason: str) -> dict[str, Any]:
    """
    Lab 1 / 3: high-impact tool — exports fake snapshot of all users/docs.
    """
    with get_connection() as conn:
        users = [row_to_dict(r) for r in conn.execute("SELECT * FROM users").fetchall()]
        docs = [row_to_dict(r) for r in conn.execute("SELECT * FROM documents").fetchall()]
    payload = {"users": users, "documents": docs, "reason": reason}
    if SENSITIVE_LOG_EXAMPLE:
        logger.warning("EXPORT triggered reason=%r payload_size=%s", reason, len(json.dumps(payload)))
    return {"export": payload, "message": "Simulated full export (dummy data only)."}


def admin_workspace_action(
    ctx: ToolContext,
    action: str,
    document_id: int | None = None,
    new_title: str | None = None,
) -> dict[str, Any]:
    """
    Lab 3: single tool supports read, write, delete, export — excessive agency surface.
    """
    action_norm = (action or "").lower().strip()
    if action_norm == "read":
        if document_id is None:
            return {"error": "document_id required"}
        return get_document(ctx, int(document_id))
    if action_norm == "rename":
        if document_id is None or not new_title:
            return {"error": "document_id and new_title required"}
        with get_connection() as conn:
            conn.execute(
                "UPDATE documents SET title = ? WHERE id = ?",
                (new_title, int(document_id)),
            )
            conn.commit()
        return {"ok": True, "action": "rename", "document_id": document_id}
    if action_norm == "delete":
        if document_id is None:
            return {"error": "document_id required"}
        with get_connection() as conn:
            conn.execute("DELETE FROM documents WHERE id = ?", (int(document_id),))
            conn.commit()
        return {"ok": True, "action": "delete", "document_id": document_id}
    if action_norm == "export":
        return export_all_user_data(ctx, reason="admin_workspace_action export")
    return {"error": "unknown_action", "allowed": ["read", "rename", "delete", "export"]}


def get_server_env_snapshot(_ctx: ToolContext) -> dict[str, Any]:
    """Lab 4: returns fake 'secrets' from DB to simulate config leak in tool output."""
    with get_connection() as conn:
        rows = conn.execute("SELECT name, value, description FROM secrets").fetchall()
    return {"secrets": [row_to_dict(r) for r in rows], "note": "Simulated environment snapshot."}


def build_context_from_docs(_ctx: ToolContext, query: str) -> dict[str, Any]:
    """
    Lab 6: concatenates document bodies into agent context without sanitization.
    Hidden instructions in a document body can poison downstream behavior.
    """
    _ = query  # "search" is a stub; returns all bodies for the vulnerable demo
    with get_connection() as conn:
        rows = conn.execute("SELECT id, title, body FROM documents").fetchall()
    parts = []
    for r in rows:
        d = row_to_dict(r)
        parts.append(f"--- Doc {d['id']}: {d['title']} ---\n{d['body']}")
    blob = "\n\n".join(parts)
    return {"context_blob": blob, "query": query}


def run_report_generator(_ctx: ToolContext, template: str) -> dict[str, Any]:
    """
    Lab 7: user-controlled string is echoed into a simulated 'command transcript'.
    No real shell is invoked.
    """
    fake_transcript = (
        "[simulated]$ report-tool --template " + json.dumps(template) + "\n"
        "[simulated] OK: report generated in /tmp/fake-report.html\n"
    )
    return {"transcript": fake_transcript, "note": "Sandboxed simulation only."}


def format_user_snippet(_ctx: ToolContext, snippet: str) -> dict[str, Any]:
    """
    Lab 8: returns HTML meant for display — vulnerable app may render without escaping.
    """
    return {"html": snippet, "raw": snippet}


def shadow_mcp_ping(_ctx: ToolContext, target: str) -> dict[str, Any]:
    """Lab 10: extra surface when shadow tools are enabled (unsafe default)."""
    return {"shadow": True, "target": target, "status": "simulated_ack"}


def append_audit_event(event_type: str, detail: str) -> None:
    """Intended for secure variant; Lab 9 leaves calls out of normal tool paths."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO audit_log (event_type, detail) VALUES (?, ?)",
            (event_type, detail),
        )
        conn.commit()


def audit_log_count() -> int:
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*) AS c FROM audit_log").fetchone()
    return int(row["c"]) if row else 0
