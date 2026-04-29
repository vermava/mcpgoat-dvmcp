"""Intentionally weak defaults for educational Lab 10."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    data_dir: Path = Path(__file__).resolve().parent / "data"
    database_path: Path = data_dir / "lab.sqlite3"

    # Lab 10: unsafe defaults (verbose errors, debug, permissive behavior)
    debug_mode: bool = True
    expose_stack_traces: bool = True
    cors_allow_all: bool = True
    enable_shadow_tools: bool = True
    max_tool_calls_per_request: int = 0  # 0 = unlimited (bad)


settings = Settings()
