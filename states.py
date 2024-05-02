from aiogram.fsm.state import State, StatesGroup
fields = ["Производство", "Торговля", "Оказание услуг", "Нет бизнеса🙅"]

class PhotoEnum:
    reg_example = "reg_example.png"
    default_photo = "default_photo.png"

class RegistrationState(StatesGroup):
    name = State()
    age = State()
    city = State()
    field = State()
    about = State()

class AdminState(StatesGroup):
    moderate = State()
    moderate_reject = State()
    mailing_text = State()