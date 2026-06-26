from pathlib import Path

from pydantic import AliasChoices, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    telegram_token: SecretStr = Field(
        validation_alias=AliasChoices("TELEGRAM_BOT_TOKEN", "ARENA_BOT_TELEGRAM_TOKEN")
    )
    arena_base_url: str = Field(
        default="https://arena.ai/text/direct",
        validation_alias=AliasChoices("ARENA_BASE_URL", "ARENA_BOT_ARENA_BASE_URL"),
    )
    storage_state_path: Path = Field(
        default=Path("sessions/main_account/storage_state.json"),
        validation_alias=AliasChoices(
            "ARENA_STORAGE_STATE_PATH", "ARENA_BOT_STORAGE_STATE_PATH"
        ),
    )
    account_metadata_path: Path = Field(default=Path("sessions/main_account/account.json"))
    sessions_root: Path = Field(
        default=Path("sessions/users"),
        validation_alias=AliasChoices("ARENA_SESSIONS_ROOT"),
    )
    log_dir: Path = Field(default=Path("logs"))
    headless: bool = Field(default=True, validation_alias=AliasChoices("ARENA_HEADLESS"))
    log_level: str = Field(default="INFO", validation_alias=AliasChoices("ARENA_LOG_LEVEL"))
    message_timeout_sec: int = Field(
        default=180, validation_alias=AliasChoices("ARENA_MESSAGE_TIMEOUT_SEC")
    )
    confirmation_timeout_sec: int = Field(
        default=180, validation_alias=AliasChoices("ARENA_CONFIRMATION_TIMEOUT_SEC")
    )
    browser_slow_mo_ms: int = Field(default=0, validation_alias=AliasChoices("ARENA_SLOW_MO_MS"))
    telegram_edit_interval_sec: float = 1.2
    verification_public_scheme: str = Field(
        default="http", validation_alias=AliasChoices("ARENA_VERIFY_PUBLIC_SCHEME")
    )
    verification_public_host: str | None = Field(
        default=None, validation_alias=AliasChoices("ARENA_VERIFY_PUBLIC_HOST")
    )
    verification_port_start: int = Field(
        default=6080, validation_alias=AliasChoices("ARENA_VERIFY_PORT_START")
    )
    verification_port_end: int = Field(
        default=6099, validation_alias=AliasChoices("ARENA_VERIFY_PORT_END")
    )
    verification_vnc_port_start: int = Field(
        default=5900, validation_alias=AliasChoices("ARENA_VERIFY_VNC_PORT_START")
    )

    @property
    def telegram_bot_token(self) -> str:
        return self.telegram_token.get_secret_value()

    @field_validator("arena_base_url")
    @classmethod
    def normalize_url(cls, value: str) -> str:
        return value if value.endswith("/") else f"{value}/"
