from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_filters_keyboard() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="Возраст", callback_data="filters:age"))
    kb.add(types.InlineKeyboardButton(text="Сфера деятельности", callback_data="filters:field"))
    kb.add(types.InlineKeyboardButton(text="Меню", callback_data="menu"))
    kb.adjust(2, 1)
    return kb.as_markup()

def get_age_keyboard(ages:dict[str:bool]) -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for k,v in ages.items():
        kb.add(types.InlineKeyboardButton(text=f"{k} {'✅' if v else '❌'}", callback_data=f"filters:edit:age:{k}"))
    kb.add(types.InlineKeyboardButton(text="Подтвердить", callback_data="filters:confirm"))
    kb.adjust(1, repeat=True)
    return kb.as_markup()

def get_field_keyboard(fields:dict[str:bool]) -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for k,v in fields.items():
        kb.add(types.InlineKeyboardButton(text=f"{k} {'✅' if v else '❌'}", callback_data=f"filters:edit:field:{k}"))
    kb.add(types.InlineKeyboardButton(text="Подтвердить", callback_data="filters:confirm"))
    kb.adjust(1, repeat=True)
    return kb.as_markup()