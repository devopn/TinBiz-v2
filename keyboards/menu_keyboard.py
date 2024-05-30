from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder    

def get_menu_keyboard() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="Изменить анкету", callback_data="edit_profile"))
    kb.add(types.InlineKeyboardButton(text="Настроить критерии поиска", callback_data="filters"))
    kb.add(types.InlineKeyboardButton(text="Начать поиск", callback_data="search:next"))
    kb.adjust(2,1)
    return kb.as_markup()