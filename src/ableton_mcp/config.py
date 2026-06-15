"""Configuration management for Ableton MCP server."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""

    ableton_ip: str = "127.0.0.1"
    ableton_send_port: int = 11000
    ableton_recv_port: int = 11001
    osc_timeout_seconds: float = 2.0
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
