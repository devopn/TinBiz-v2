from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from states import fields
def get_fields_keyboard() -> types.ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for i in fields:
        kb.add(types.KeyboardButton(text=i))
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)