import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from _bot.handlers_global import router as global_router
from _bot.handlers_bybit import router as bybit_router
import config

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Include all routers
    dp.include_router(global_router)
    dp.include_router(bybit_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
