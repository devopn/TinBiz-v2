from aiogram.fsm.state import State, StatesGroup
fields = ["Производство", "Торговля", "Оказание услуг", "Нет бизнеса🙅"]
ages = ["10-20", "21-30", "31-50", "51-80", "81-90"]   
class PhotoEnum:
    reg_example = "reg_example.png"
    default_photo = "default_photo.png"

class RegistrationState(StatesGroup):
    name = State()
    age = State()
    city = State()
    field = State()
    about = State()

class ProfileEditState(StatesGroup):
    state = State()
    name = State()
    age = State()
    city = State()
    photo = State()
    field = State()
    about = State()

class AdminState(StatesGroup):
    moderate = State()
    moderate_reject = State()
    mailing_text = State()