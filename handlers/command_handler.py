from aiogram import Router, types, F
from aiogram.filters import Command
from db.models import *
from db import service
from states import RegistrationState
from aiogram.fsm.context import FSMContext
router = Router()

from keyboards.cancel_moderate_keyboard import get_cancel_moderate_keyboard
from keyboards.menu_keyboard import get_menu_keyboard
@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    user = await service.get_user(id=message.from_user.id)
    if user is None:
        await message.answer("*Добро пожаловать!*\n@TinBiz\_bot - бот для знакомств предпринимателей.", parse_mode="Markdown")
        await state.set_state(RegistrationState.name)
        await message.answer("🔖<b>Регистрация</b>\nШаг 1 из 5\n<i>Пожалуйста, введите ваше имя</i>", parse_mode="HTML")
    elif not user.moderated:
        await message.answer("Ваша анкета на рассмотрении", reply_markup=get_cancel_moderate_keyboard())
    else:
        await message.answer_photo(photo=user.photo, caption=str(user), reply_markup=get_menu_keyboard())

