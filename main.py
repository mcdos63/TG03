import asyncio, aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from config import *

logging.basicConfig(level=logging.INFO)
class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)
@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)
@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("В каком классе учишься?")
    await state.set_state(Form.grade)
@dp.message(Form.grade)
async def grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, age, grade) VALUES (?, ?, ?)", (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()
    await message.answer("Спасибо за ответы!\n")
    async with aiohttp.ClientSession() as session:
        weather_data = await get_weather()  # Получаем данные о погоде из функции get_weather() в config.py
        weather = weather_data['описание']
        temperature = weather_data['температура']
        humidity = weather_data['влажность']
        weather_report = f"Погода: {weather}, {temperature}, {humidity}"
        await message.answer(weather_report)
    await state.clear()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    init_db()
    asyncio.run(main())
