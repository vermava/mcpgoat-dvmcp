"""Example: object-level authorization for a document read tool."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass


@dataclass
class ToolContext:
    user_id: int
    username: str


def get_document_secure(conn: sqlite3.Connection, ctx: ToolContext, document_id: int) -> dict:
    row = conn.execute(
        """
        SELECT id, owner_user_id, title, body
        FROM documents
        WHERE id = ?
        """,
        (document_id,),
    ).fetchone()
    if not row:
        return {"error": "not_found"}
    owner_id = row["owner_user_id"]
    if owner_id != ctx.user_id:
        return {"error": "forbidden"}
    return {"document": dict(row)}
