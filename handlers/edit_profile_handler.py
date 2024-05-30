from aiogram import Router, types, F
from db import service
from aiogram.filters.state import StateFilter
from db.models import *
from aiogram.fsm.context import FSMContext
from keyboards.edit_profile_keyboard import get_edit_profile_keyboard
from keyboards.fields_keyboard import get_fields_keyboard
from states import ProfileEditState, fields
router = Router()

@router.callback_query(F.data == "edit_profile")
async def edit_profile(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    user = await service.get_user(call.from_user.id)
    await call.answer()
    await call.message.answer("Что вы хотите изменить?\n\nВаша анкета:\n" + str(user), reply_markup=get_edit_profile_keyboard())

@router.callback_query(F.data.startswith("edit_profile:"))
async def edit_profile_choose(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    action = call.data.split(":")[1]
    match action:
        case "name":
            await call.message.answer("Новое имя:")
            await state.set_state(ProfileEditState.name)
        case "age":
            await call.message.answer("Новый возраст:")
            await state.set_state(ProfileEditState.age)
        case "city":
            await call.message.answer("Новый город:")
            await state.set_state(ProfileEditState.city)
        case "field":
            await call.message.answer("Новая сфера деятельности:", reply_markup=get_fields_keyboard())
            await state.set_state(ProfileEditState.field)
        case "about":
            await call.message.answer("Новый о себе:")
            await state.set_state(ProfileEditState.about)
        case "photo":
            await call.message.answer("Новое фото:")
            await state.set_state(ProfileEditState.photo)
        case "state":
            user = await service.get_user(call.from_user.id)
            await service.update_user(call.from_user.id, active=not user.active)
            user.active = not user.active
            await call.message.edit_text("Что вы хотите изменить?\n\nВаша анкета:\n" + str(user), reply_markup=get_edit_profile_keyboard())
        case "history":
            await service.delete_search(call.from_user.id)
            await call.message.edit_text("История очищена! Что дальше?", reply_markup=get_edit_profile_keyboard())
        
@router.message(StateFilter(ProfileEditState))
async def edit_profile_save(message: types.Message, state: FSMContext):
    states = await state.get_state()
    match states:
        case ProfileEditState.name:
            await service.update_user(message.from_user.id, name=message.text)
        case ProfileEditState.age:
            if (not message.text.isdigit()) or (not 10 <= int(message.text) < 100):
                await message.answer("Неверный возраст")
                return
            await service.update_user(message.from_user.id, age=int(message.text))
        case ProfileEditState.city:
            await service.update_user(message.from_user.id, city=message.text)
        case ProfileEditState.field:
            if message.text not in fields:
                await message.answer("Неверная сфера деятельности")
            await service.update_user(message.from_user.id, field=message.text)
        case ProfileEditState.photo:
            photo = message.photo[-1].file_id
            if not photo:
                await message.answer("Неверное фото")
                return
            await service.update_user(message.from_user.id, photo=photo)
        case ProfileEditState.about:
            await service.update_user(message.from_user.id, about=message.text)
    await state.clear()
    await message.answer("Ваша анкета была обновлена", reply_markup=types.ReplyKeyboardRemove())
    user = await service.get_user(message.from_user.id)
    await message.answer("Что вы хотите изменить?\n\nВаша анкета:\n" + str(user), reply_markup=get_edit_profile_keyboard())
