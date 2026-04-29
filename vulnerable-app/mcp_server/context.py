"""Per-request context for MCP tool handlers."""

from dataclasses import dataclass


@dataclass
class ToolContext:
    """Who is acting and which lab scenario is active."""

    user_id: int
    username: str
    lab_id: int = 0
