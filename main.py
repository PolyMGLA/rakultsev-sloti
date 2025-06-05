import os
import dotenv

import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

from games import slots, blackjack
from db.database import CasinoBase

dotenv.load_dotenv()

RULES = "\n\n".join([slots.RULES, blackjack.RULES])
HELP = """
Казино Ракульцев

/start - регистрация
/profile - ваш профиль
/help - помощь
/rules - правила игр
/slots - крутить слоты
/dodep - додеп
"""

db = CasinoBase()
db.init()

BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def gay_start(msg: types.Message):
    if db.register(msg.from_user.id, msg.from_user.full_name):
        await msg.answer("Регистрация успешна!\n/help - список команд")
    else:
        await msg.answer("Регистрация не удалась, поплачь(\n/help - список команд")

@dp.message(Command("help"))
async def gay_help(msg: types.Message):
    await msg.answer(HELP)

@dp.message(Command("profile"))
async def gay_profile(msg: types.Message):
    user = db.get_user(msg.from_user.id)
    if user is None or user == False:
        await msg.answer("Вы не зарегистрированы!\n/start")
    await msg.answer(f"Пользователь: {user.name}\nБаланс: {user.balance}" + ("(вы в долгах)" if user.balance < 0 else "") + f"\nМаксимальный баланс: {user.maxbal}")

@dp.message(Command("rules"))
async def gay_ref(msg: types.Message):
    await msg.answer(RULES)

@dp.message(Command("slots"))
async def gay_spin(msg: types.Message):
    msgs = slots.spin(db, msg.from_user.id)
    for m in msgs:
        await msg.answer(m)

@dp.message(Command("dodep"))
async def gay_dodep(msg: types.Message):
    if db.update_bal(msg.from_user.id, 100):
        await msg.answer("додеп прошел")
    else:
        await msg.answer("додеп не прошел")

async def main():
    print("starting bot..")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())