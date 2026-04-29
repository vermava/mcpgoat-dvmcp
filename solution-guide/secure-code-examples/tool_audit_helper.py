"""Example: append-only audit helper for MCP tool invocations."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import UTC, datetime
from typing import Any


def hash_args(arguments: dict[str, Any]) -> str:
    payload = json.dumps(arguments, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def audit_tool_call(
    conn: sqlite3.Connection,
    *,
    actor_id: int,
    tool_name: str,
    arguments: dict[str, Any],
    outcome: str,
) -> None:
    conn.execute(
        """
        INSERT INTO audit_log (event_type, detail)
        VALUES (?, ?)
        """,
        (
            "mcp.tool_call",
            json.dumps(
                {
                    "ts": datetime.now(tz=UTC).isoformat(),
                    "actor_id": actor_id,
                    "tool": tool_name,
                    "args_sha256": hash_args(arguments),
                    "outcome": outcome,
                }
            ),
        ),
    )
    conn.commit()
