from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *


api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Регистрация"),
            KeyboardButton(text="Рассчитать")
        ],
        [
            KeyboardButton(text="Информация"),
            KeyboardButton(text="Купить")
        ]
    ], resize_keyboard=True
)

catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product2', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product3', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product4', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product5', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product6', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product7', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product8', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product9', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product10', callback_data='product_buying')]
    ]
)

inline_kb = InlineKeyboardMarkup()
in_but1 = InlineKeyboardButton(text = "Рассчитать норму калорий", callback_data='calories')
in_but2 = InlineKeyboardButton(text = "Формулы расчёта", callback_data='formulas')

inline_kb.add(in_but1)
inline_kb.add(in_but2)

class RegistrationState(StatesGroup):
    username = State()
    email_name = State()
    age = State()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


products = get_all_products()


@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):

    if is_included(message.text) is None or False:
        await state.update_data(username=message.text)
        await message.answer(f"Здравствуйте {message.text}! \nВведите свой email: ")
        await RegistrationState.email_name.set()
    else:
        await message.answer(f"Пользователь {message.text} существует! введите другое имя.\n")

@dp.message_handler(state=RegistrationState.email_name)
async def set_email(message, state):
    await state.update_data(email_name=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    print(data['username'], data['email_name'], data['age'])
    add_user(data['username'], data['email_name'], data['age'])
    await message.answer(f" Пользователь -  {data['username']}, вы успешно прошли регшистрацию!", reply_markup=kb)


@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Привет бот помогает твоему здовроью, однако! ", reply_markup=kb)

@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию::", reply_markup=inline_kb)

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x A;')
    await call.message.answer('для женщин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) – 161) x A.')
    await call.answer()



@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")

@dp.message_handler(text="Информация")
async def inform(message):
    await message.answer('Инфо про бот')

@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = ((10 * int(data['weight'])) + (6.25 * int(data['growth'])) - (5 * int(data['age'])) + 5)
    await message.answer(f'Вашша норма калорий {calories}')
    await state.finish()

@dp.message_handler(text = 'Купить')
async def get_buying_list(message):
    pic = 1
    for i in products:
        await message.answer(f'Название: {i[0]} | Описание: {i[1]} | Цена: {i[2]}')
        with open(f'{pic}.jpeg', 'rb') as img:
            await message.answer_photo(img)
            pic += 1
            #buy_text = f"Название: Product{i} | Описание: описание {i} | Цена: {i * 100}."
            #await message.answer_photo(img, buy_text)
    await message.answer("Выберите продукт для покупки:", reply_markup=catalog_kb)



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

