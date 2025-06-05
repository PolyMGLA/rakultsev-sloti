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
/top - топ казино
"""

db = CasinoBase()
db.init()

BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def gay_start(msg: types.Message):
    if db.register(msg.from_user.id, "@" + msg.from_user.username):
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
    await msg.answer(
        f"Пользователь: {user.name}"
         + f"\nБаланс: {user.balance}" + ("(вы в долгах)" if user.balance < 0 else "")
         + f"\nКруток слотов: {user.slots_num}"
         + f"\nДодепов: {user.dodep_num}"
        )

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
        if db.add_dodep(msg.from_user.id):
            await msg.answer("додеп прошел")
        else:
            await msg.answer("додеп не прошел")
    else:
        await msg.answer("додеп не прошел")

@dp.message(Command("top"))
async def gay_top(msg: types.Message):
    top = db.top5_money()
    res = ""

    res += "Топ по счету:\n"
    if top == False:
        res += "ашипка\n\n"
    else:
        res += "\n".join([f"{i + 1}. {top[i].name} - {top[i].balance}" for i in range(len(top))]) + "\n\n"

    top = db.top5_slots()
    res += "Топ по круткам:\n"
    if top == False:
        res += "ашипка\n\n"
    else:
        res += "\n".join([f"{i + 1}. {top[i].name} - {top[i].slots_num}" for i in range(len(top))]) + "\n\n"
    
    top = db.top5_dodeps()
    res += "Топ по додепам:\n"
    if top == False:
        res += "ашипка\n\n"
    else:
        res += "\n".join([f"{i + 1}. {top[i].name} - {top[i].dodep_num}" for i in range(len(top))]) + "\n\n"

    await msg.answer(res)

async def main():
    print("starting bot..")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())