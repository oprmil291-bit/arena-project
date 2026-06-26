import asyncio
import os
import sys
from pathlib import Path

from pydantic import SecretStr

from arena_proxy_bot.arena.session_manager import (
    ArenaAutomationError,
    ArenaSessionManager,
    ArenaVerificationRequired,
)
from arena_proxy_bot.config import Settings


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


async def main() -> int:
    prompt = " ".join(sys.argv[1:]).strip() or "How many hours are in a day? Answer briefly."
    settings = Settings(
        telegram_token=SecretStr(os.getenv("TELEGRAM_BOT_TOKEN", "dummy")),
        arena_base_url=os.getenv("ARENA_BASE_URL", "https://arena.ai/text/direct"),
        sessions_root=Path(os.getenv("ARENA_SESSIONS_ROOT", "sessions/smoke")),
        headless=_env_bool("ARENA_HEADLESS", False),
        message_timeout_sec=int(os.getenv("ARENA_MESSAGE_TIMEOUT_SEC", "90")),
    )
    user_id = int(os.getenv("ARENA_SMOKE_USER_ID", "900001"))
    manager = ArenaSessionManager(settings)

    try:
        chunks: list[str] = []
        async for chunk in manager.stream_answer(user_id, prompt):
            chunks.append(chunk)
            print(f"CHUNK: {chunk[:1000]}", flush=True)
        print(f"FINAL: {chunks[-1] if chunks else '<empty>'}", flush=True)
        return 0
    except ArenaVerificationRequired as exc:
        print(f"VERIFY_REQUIRED: {exc}", flush=True)
        return 2
    except ArenaAutomationError as exc:
        print(f"AUTOMATION_ERROR: {exc}", flush=True)
        return 3
    finally:
        await manager.close()


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
