from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_edit_profile_keyboard() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="Имя", callback_data="edit_profile:name"))
    kb.add(types.InlineKeyboardButton(text="Возраст", callback_data="edit_profile:age"))
    kb.add(types.InlineKeyboardButton(text="Город", callback_data="edit_profile:city"))
    
    kb.add(types.InlineKeyboardButton(text="О себе", callback_data="edit_profile:about"))
    kb.add(types.InlineKeyboardButton(text="Фото", callback_data="edit_profile:photo"))
    kb.add(types.InlineKeyboardButton(text="Сферу деятельности", callback_data="edit_profile:field"))
    kb.add(types.InlineKeyboardButton(text="Переключить состояние анкеты", callback_data="edit_profile:state"))
    kb.add(types.InlineKeyboardButton(text="Очистить историю поиска", callback_data="edit_profile:history"))
    kb.add(types.InlineKeyboardButton(text="В меню", callback_data="menu"))
    kb.adjust(3,2,1,1,1)
    return kb.as_markup()