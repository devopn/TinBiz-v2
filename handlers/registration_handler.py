from aiogram import Router, types, F
from aiogram.filters import StateFilter
from db.models import *
from db import service
from states import RegistrationState
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendPhoto

router = Router()

from keyboards.fields_keyboard import get_fields_keyboard
from states import fields, PhotoEnum

@router.message(StateFilter(RegistrationState.name))
async def reg_name(message: types.Message, state:FSMContext):
    await state.update_data(name=message.text)
    await message.answer("🔖<b>Регистрация</b>\nШаг 2 из 5\n<i>Введите ваш возраст</i>", parse_mode="HTML")
    await state.set_state(RegistrationState.age)


@router.message(StateFilter(RegistrationState.age))
async def reg_age(message: types.Message, state:FSMContext):
    data = message.text
    if not data.isdigit():
        await message.answer("🔖<b>Регистрация</b>\nШаг 2 из 5\n<i>Возраст должен быть числом</i>", parse_mode="HTML")
    elif not 10 <= int(data) < 100:
        await message.answer("🔖<b>Регистрация</b>\nШаг 2 из 5\n<i>Возраст должен быть от 10 до 99</i>", parse_mode="HTML")
    else:
        await state.update_data(age=int(data))
        await message.answer("🔖<b>Регистрация</b>\nШаг 3 из 5\n<i>В каком городе вы живете?</i>", parse_mode="HTML")
        await state.set_state(RegistrationState.city)

@router.message(StateFilter(RegistrationState.city))
async def reg_city(message: types.Message, state:FSMContext):
    await state.update_data(city=message.text)
    await message.answer("🔖<b>Регистрация</b>\nШаг 4 из 5\n<i>Ваша сфера деятельности:</i>", parse_mode="HTML", reply_markup=get_fields_keyboard())
    await state.set_state(RegistrationState.field)

@router.message(StateFilter(RegistrationState.field))
async def reg_field(message: types.Message, state:FSMContext):
    data = message.text
    if data not in fields:
        await message.answer("🔖<b>Регистрация</b>\nШаг 4 из 5\n<i>Некорректная сфера деятельности</i>", parse_mode="HTML", reply_markup=get_fields_keyboard())
    else:
        await state.update_data(field=data)

        reg_image:Image = await service.get_image(PhotoEnum.reg_example)
        if reg_image is None:
            data = types.FSInputFile(f"img/{PhotoEnum.reg_example}")
            photo = await message.answer_photo(data)

            await service.create_image(PhotoEnum.reg_example, photo.photo[0].file_id)
        else:
            await message.answer_photo(photo=reg_image.id)

        await message.answer("🔖<b>Регистрация</b>\nШаг 5 из 5\n<i>Пожалуйста, расскажите о себе (какой опыт в бизнесе, ваши интересы)  </i>", parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(RegistrationState.about)

@router.message(StateFilter(RegistrationState.about))
async def reg_about(message: types.Message, state:FSMContext):
    await state.update_data(about=message.text)
    data = await state.get_data()
    photos = await message.from_user.get_profile_photos().bot.get_user_profile_photos(message.from_user.id)

    if len(photos.photos) == 0:
        photo = await service.get_image(PhotoEnum.default_photo)
        if photo is None:
            data = types.FSInputFile(f"img/{PhotoEnum.default_photo}")
            photo = await message.answer_photo(data)
            await service.create_image(PhotoEnum.default_photo, photo.photo[0].file_id)
            photo = photo.photo[0].file_id
    else:
        photo = photos.photos[0][0].file_id
    
    user = User(
        id = message.from_user.id,
        name = data.get("name", "Без имени"),
        username = message.from_user.username,
        age = data.get("age", 18),
        city = data.get("city", "Без города"),
        field = data.get("field", "Без сферы"),
        about = data.get("about", "Без описания"),
        photo = photo
    )
    await service.create_user(user)
    await state.clear()
    await message.answer("Анкету получили, спасибо! Её проверка займёт до двух рабочих дней, но мы постараемся быстрее. О результате напишем в этот бот.", parse_mode="HTML")


@router.callback_query(F.data == "cancel_moderate")
async def cancel_moderate(call: types.CallbackQuery):
    await service.delete_user(id=call.from_user.id)
    await call.answer()
    await call.message.answer("Ваша анкета отменена. Спасибо, что воспользовались нашим ботом!", reply_markup=types.ReplyKeyboardRemove())
