import sys

from loguru import logger

from arena_proxy_bot.config import Settings


def configure_logging(settings: Settings) -> None:
    settings.log_dir.mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(sys.stderr, level=settings.log_level, enqueue=True, backtrace=False, diagnose=False)
    logger.add(
        settings.log_dir / "bot.log",
        level=settings.log_level,
        rotation="20 MB",
        retention="14 days",
        compression="zip",
        enqueue=True,
        backtrace=False,
        diagnose=False,
    )
