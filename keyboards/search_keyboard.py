from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_search_keyboard(can_id) -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="Связаться", callback_data=f"search:contact:{can_id}"))
    kb.add(types.InlineKeyboardButton(text="Дальше", callback_data="search:next"))
    kb.add(types.InlineKeyboardButton(text="В меню", callback_data="menu"))
    kb.adjust(2,1)
    return kb.as_markup()

def get_search_keyboard_short() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="Дальше", callback_data="search:next"))
    kb.add(types.InlineKeyboardButton(text="В меню", callback_data="menu"))
    kb.adjust(2,1)
    return kb.as_markup()