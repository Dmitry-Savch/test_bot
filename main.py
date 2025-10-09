import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from _bot.handlers_global import router as global_router
from _bot.handlers_bybit import router as bybit_router
# from _bot.handlers_mexc import router as mexc_router  # TODO: Update MEXC handlers
import config

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Include all routers
    dp.include_router(global_router)
    dp.include_router(bybit_router)
    # dp.include_router(mexc_router)  # TODO: Update MEXC handlers

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
