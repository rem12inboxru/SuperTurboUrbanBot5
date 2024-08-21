from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формула расчета', callback_data='formulas')
kb.add(button1)
kb.add(button2)

kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
button11 = KeyboardButton(text='Рассчитать')
button12 = KeyboardButton(text='Информация')
kb1.add(button11)
kb1.add(button12)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию',reply_markup=kb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью',reply_markup=kb1)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(two=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(three=message.text)
    data = await state.get_data()
    for k, v in data.items():
        data[k] = int(v)
    c = 10 * data['three'] + 6.25 * data['two'] - 5 * data['first'] + 5
    await message.answer(f'Ваша норма калорий {c}')
    await state.finish()

@dp.message_handler()
async def all_message(message):
    #print('Введите команду /start чтобы начать общение.')
    await message.answer('Введите команду /start чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
