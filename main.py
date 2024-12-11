from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from app.database import init_db
from app.handlers import orders, get_order, admin, start
from app.config import config
from logging import basicConfig, INFO
async def main():
    # Botni sozlash
    bot = Bot(token=config.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    basicConfig(level=INFO)
    # Ma'lumotlar bazasini yaratish

    # Komandalar ro'yxatini sozlash
    await bot.set_my_commands([
        BotCommand(command="/start", description="Botni ishga tushirish"),
    ])

    # Handlerlarni ro'yxatdan o'tkazish
    dp.include_router(start.router)
    dp.include_router(orders.router)
    dp.include_router(get_order.router)
    dp.include_router(admin.router)

    # Botni ishga tushirish
    await dp.start_polling(bot)

if __name__ == "__main__":
    init_db()
    import asyncio
    asyncio.run(main())
