from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder    

def get_menu_keyboard() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="Изменить анкету", callback_data="menu"))
    kb.add(types.InlineKeyboardButton(text="Настроить критерии поиска", callback_data="menu"))
    kb.add(types.InlineKeyboardButton(text="Начать поиск", callback_data="menu"))
    kb.adjust(2,1)
    return kb.as_markup()