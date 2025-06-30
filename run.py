import asyncio
import logging
import sys
from pathlib import Path
from aiogram import Bot, Dispatcher

sys.path.append(str(Path(__file__).parent))

from config import TOKEN
from routers import main_router  

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(main_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")