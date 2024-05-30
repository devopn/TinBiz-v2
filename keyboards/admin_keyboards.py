from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_admin_main_keyboard() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="Модерация", callback_data="admin:moderate"))
    kb.add(types.InlineKeyboardButton(text="Отправить рассылку", callback_data="admin:mailing"))
    kb.add(types.InlineKeyboardButton(text="Выход", callback_data="menu"))
    kb.adjust(2,1)
    return kb.as_markup()

def get_admin_moderation_keyboard() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="Одобрить", callback_data="accept"))
    kb.add(types.InlineKeyboardButton(text="Стоп", callback_data="stop"))
    kb.add(types.InlineKeyboardButton(text="Отклонить", callback_data="reject"))
    return kb.as_markup()