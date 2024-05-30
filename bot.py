import asyncio
import logging

# Aiogram imports
from aiogram import Dispatcher, Bot, types, enums
import aiogram

# Routers
from handlers.command_handler import router as command_router
from handlers.registration_handler import router as registration_router
from handlers.menu_handler import router as menu_router
from handlers.admin_handler import router as admin_router
from handlers.edit_profile_handler import router as edit_profile_router
from handlers.filter_handler import router as filter_router
from handlers.search_handler import router as search_router
from config import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


async def main():

    # Set up bot
    bot = Bot(token=config.tg_token)
    await bot.set_my_commands(
        commands=[
            types.BotCommand(command="start", description="Перезапуск бота "),
            types.BotCommand(command="help", description="Справка"),
            types.BotCommand(command="menu", description="Меню"),
            types.BotCommand(command="profile", description="Изменить информацию профиля"),
            types.BotCommand(command="hide", description="Скрыть анкету"),
            types.BotCommand(command="criteria", description="Изменить критерии поиска"),
            types.BotCommand(command="start_search", description="Начать поиск собеседника"),
            ]
    )

    dp = Dispatcher()
    dp.include_routers(command_router, registration_router, menu_router, admin_router, edit_profile_router, filter_router, search_router)

    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())