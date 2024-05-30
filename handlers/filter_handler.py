from aiogram import types, Router, F
from db import service
from db.models import *
from states import ages, fields
from aiogram.fsm.context import FSMContext
from keyboards.filter_keyboard import get_filters_keyboard, get_age_keyboard, get_field_keyboard

router = Router()

@router.callback_query(F.data == "filters")
async def filters_callback(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    user = await service.get_user(call.from_user.id)
    filters = dict(user.filters)
    await state.update_data(filters=filters)
    await call.message.answer("Выбери по каким критериям ты хочешь фильтровать?", reply_markup=get_filters_keyboard())

@router.callback_query(F.data.startswith("filters:")) 
async def filters_choose(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("filters"):
        await call.message.answer("Произошла ошибка, попробуй еще раз")
        return
    filters:dict = data["filters"]
    await call.answer()
    action = call.data.split(":")[1]
    match action:
        case "age":
            await call.message.edit_text("Возраст:", reply_markup=get_age_keyboard(filters.get("age")))
        case "field":
            await call.message.edit_text("Сфера деятельности:", reply_markup=get_field_keyboard(filters.get("field")))
        case "confirm":
            await service.update_user(call.from_user.id, filters=data["filters"])
            await call.message.edit_text("Выбери по каким критериям ты хочешь фильтровать?", reply_markup=get_filters_keyboard())
        case "edit":
            subj = call.data.split(":")[2]
            val = call.data.split(":")[3]
            filters[subj][val] = not filters[subj][val]
            await state.update_data(filters=filters)
            if subj == "age":
                await call.message.edit_text("Возраст:", reply_markup=get_age_keyboard(filters.get("age")))
            if subj == "field":
                await call.message.edit_text("Сфера деятельности:", reply_markup=get_field_keyboard(filters.get("field")))