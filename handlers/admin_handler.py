from aiogram import Router, types, F
from keyboards.admin_keyboards import *
from aiogram.fsm.context import FSMContext
from states import AdminState
from db import service

from aiogram.filters import Command

from aiogram.filters.state import StateFilter
router = Router()

@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    admins = await service.get_admins()
    if not message.from_user.id in admins:
        return
    await message.answer("Админ панель", reply_markup=get_admin_main_keyboard())

@router.callback_query(F.data.startswith("admin"))
async def admin_callback(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    action = call.data.split(":")[1]
    match action:
        case "menu":
            await call.message.answer("Админ панель", reply_markup=get_admin_main_keyboard())
        case "moderate":
            await state.set_state(AdminState.moderate)
            await call.message.answer("Модерация", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="Начать", callback_data="start")]]))
        case "mailing":
            await state.set_state(AdminState.mailing_text)
            await call.message.answer("Текст рассылки:")

@router.message(StateFilter(AdminState.mailing_text))
async def mailing_text(message: types.Message, state: FSMContext):
    text = message.text
    await state.clear()
    await service.send_mailing(message.bot, text)
    await message.answer("Рассылка была отправлена")

@router.callback_query(StateFilter(AdminState.moderate))
async def moderate_callback(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    action = call.data
    data = await state.get_data()
    match action:
        case "accept":
            try:
                await service.accept_candidate(data.get("candidate_id"))
                await call.bot.send_message(chat_id=data.get("candidate_id"), text="Ваша анкета была одобрена. Можете начинать пользоваться ботом. /menu")
            except Exception as e:
                print(e)
        case "reject":
            await call.message.answer("Причина отказа?", reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="К сожалению, информация о себе недостаточно полная, попробуйте ещё раз!")]],resize_keyboard=True))
            await state.set_state(AdminState.moderate_reject)
            return
        case "stop":
            await state.clear()
            await call.message.answer("Админ панель", reply_markup=get_admin_main_keyboard())
            return
    candidate = await service.get_moderation_candidate()
    await state.update_data(candidate_id=candidate.id)
    await call.message.answer_photo(photo=candidate.photo, caption=str(candidate), reply_markup=get_admin_moderation_keyboard())


@router.message(StateFilter(AdminState.moderate_reject))
async def reject_reason(message: types.Message, state: FSMContext):
    reason = message.text
    m = await message.answer(":)", reply_markup=types.ReplyKeyboardRemove())
    await m.delete()
    data = await state.get_data()
    candidate = await service.get_user(id=data.get("candidate_id"))
    await message.bot.send_message(chat_id=candidate.id, text=f"Ваша анкета была отклонена по причине: {reason}. Попробуйте зарегестрировать ещё раз через команду /start")
    await service.delete_user(data.get("candidate_id"))
    await state.set_state(AdminState.moderate)
    await message.answer("Продолжить?", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="Да", callback_data="start"),
                 types.InlineKeyboardButton(text="В меню", callback_data="admin:menu")]]))