from aiogram import Router, types, F
from db import service
from db.models import *
from aiogram.fsm.context import FSMContext
from keyboards.search_keyboard import get_search_keyboard, get_search_keyboard_short

router = Router()

@router.callback_query(F.data.startswith("search"))
async def search_choose(call: types.CallbackQuery, state: FSMContext):

    action = call.data.split(":")[1]
    match action:
        case "contact":
            user_id = int(call.data.split(":")[2])
            await call.answer()
            candidate = await service.get_user(user_id)
            await call.message.answer("Свяжитесь с  пользователем. Вот его аккаунт: @" + str(candidate.username), reply_markup=get_search_keyboard_short())
        case "next":
            data = await state.get_data()
            if not data.get("candidates"):
                candidates = await service.get_search(call.from_user.id)
                if not candidates:
                    await call.answer("Пользователи закончились")
                    return
                await state.update_data(candidates=candidates)
                data["candidates"] = candidates
            candidates = data.get("candidates")
            candidate = candidates.pop(0)
            if not candidate:
                candidates = await service.get_search(call.from_user.id)
                if not candidates:
                    await call.answer("Пользователи закончились")
                    return
                candidate = candidates.pop(0)
                
                data["candidates"] = candidates
            await service.add_search(call.from_user.id, candidate.id)
            await call.answer()
            await state.update_data(candidates=candidates)
            await call.message.answer_photo(photo=candidate.photo, caption=candidate.draw(), reply_markup=get_search_keyboard(candidate.id))