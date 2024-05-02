from aiogram import types, Router, F
from db import service
from db.models import *
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
router = Router()
from keyboards.menu_keyboard import get_menu_keyboard

@router.message(Command("menu"))
@router.callback_query(F.data == "menu")
async def cmd_menu(call: types.CallbackQuery, state: FSMContext):
    if type(call) == types.CallbackQuery: await call.answer()
    context = call if type(call) == types.Message else call.message
    await state.clear()
    user = await service.get_user(id=call.from_user.id)
    if (not user) or (not user.moderated):
        await context.answer("Ваша анкета еще не создана или на рассмотрении!")
    await context.answer_photo(photo=user.photo, caption=str(user), reply_markup=get_menu_keyboard())