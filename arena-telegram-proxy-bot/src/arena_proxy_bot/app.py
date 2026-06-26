import asyncio
import signal

from aiogram import Bot, Dispatcher
from loguru import logger

from arena_proxy_bot.arena.session_manager import ArenaSessionManager
from arena_proxy_bot.bot.handlers import build_router
from arena_proxy_bot.config import Settings
from arena_proxy_bot.logging_config import configure_logging


async def run() -> None:
    settings = Settings()
    configure_logging(settings)

    bot = Bot(token=settings.telegram_bot_token)
    dispatcher = Dispatcher()
    manager = ArenaSessionManager(settings)
    dispatcher.include_router(build_router(manager, settings))

    stop_event = asyncio.Event()

    def _request_stop() -> None:
        logger.info("Shutdown signal received")
        stop_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _request_stop)
        except NotImplementedError:
            signal.signal(sig, lambda *_: _request_stop())

    try:
        logger.info("Starting Telegram polling")
        polling_task = asyncio.create_task(dispatcher.start_polling(bot))
        stop_task = asyncio.create_task(stop_event.wait())
        done, pending = await asyncio.wait(
            {polling_task, stop_task},
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
        for task in done:
            task.result()
    finally:
        await manager.close()
        await bot.session.close()
        logger.info("Bot stopped")


def main() -> None:
    asyncio.run(run())
