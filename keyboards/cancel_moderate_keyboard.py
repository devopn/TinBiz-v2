from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_cancel_moderate_keyboard() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="Удалить анкету", callback_data="cancel_moderate"))
    return kb.as_markup()