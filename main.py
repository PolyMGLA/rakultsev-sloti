                                                                    #импорт всякой залупы
import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

from db import db, dt, dv
import routes.slots
import routes.admins
import routes.blackjack
from routes.keyboards import *
import config
from messages import HELP, RULES

from datetime import datetime

from bot import bot, dp


@dp.message(Command("start"))
async def gay_start(msg: types.Message):
    """
    Регистрация пользователя (попытка зарегать)
    """
    dv.set_date(msg.from_user.id)
    x = not db.register(
        msg.from_user.id,
        ("@" + msg.from_user.username) if not msg.from_user.username is None else msg.from_user.full_name
        )
    y = not dt.add_user(msg.from_user.id)
    z = not dv.add_user(msg.from_user.id)
    if x or y or z:
        await msg.answer("Регистрация успешна!\n/menu - главное меню")
    else:
        await msg.answer("Регистрация не удалась, поплачь(\n/menu - главное меню")


@dp.message(Command("visitors"))
async def gay_visitors(msg: types.Message):
    """
    Список пользователей, которые активничали последнюю минуту
    """
    dv.set_date(msg.from_user.id)
    vis = dv.get_list()
    await msg.answer(
        f"В казино: {len(vis)} человек\n" \
        + "\n".join([f"{el.user.name}" for el in vis])
    )


@dp.message(F.text.lower() == "🆘помощь🆘")
async def gay_help(msg: types.Message):
    """
    Собсна текст помощи утопающим
    """
    dv.set_date(msg.from_user.id)
    await msg.answer(HELP)


@dp.message(F.text.lower() == "👾профиль👾")
async def gay_profile(msg: types.Message):
    """
    Инфо о профиле пользователя
    """
    dv.set_date(msg.from_user.id)
    user = db.get_user(msg.from_user.id)
    if user is None or user == False:
        await msg.answer("Вы не зарегистрированы!\n/start")
    await msg.answer(
        f"Пользователь: {user.name}"
         + f"\nБаланс: {user.balance}" + (" (вы в долгах)" if user.balance < 0 else "")
         + f"\nКруток слотов: {user.slots_num}"
         + f"\nДодепов: {user.dodep_num}"
        )


@dp.message(F.text.lower() == "🔥правила🔥")
async def gay_rules(msg: types.Message):
    """
    Текст правил всех игр (мне точно надо это писать?)
    """
    dv.set_date(msg.from_user.id)
    await msg.answer(RULES)


@dp.message(F.text.lower() == "💲мега ласт деп💲")
async def gay_dodep(msg: types.Message):
    """
    Функция для пополнения баланса на аккаунте (собственно говоря, додеп)
    """
    dv.set_date(msg.from_user.id)
    user = db.get_user(msg.from_user.id)
    if user.balance < 2:
        if dt.get_date(msg.from_user.id) is None:
            dt.add_user(msg.from_user.id)

        tdt = int(datetime.now().timestamp())
        last_dodep = dt.get_date(msg.from_user.id).date
        if tdt - last_dodep < 600:
            await msg.answer(f"подождите {(600 - tdt + last_dodep) // 60} минут {(600 - tdt + last_dodep) % 60} секунд")
        else:
            if db.update_bal(msg.from_user.id, 100) and db.add_dodep(msg.from_user.id) and dt.set_date(msg.from_user.id, tdt):
                await msg.answer("додеп прошел")
            else:
                await msg.answer("додеп не прошел")
    else:
        await msg.answer("вы слишком богатые")


@dp.message(F.text.lower() == "🔝топ казино🎰")
async def gay_top(msg: types.Message):
    """
    Топ казино по балансу, круткам слотов и додепам
    """
    dv.set_date(msg.from_user.id)
    res = ""

    for nom in [
        [db.top5_money, "счету", "balance"],
        [db.top5_slots, "круткам", "slots_num"],
        [db.top5_dodeps, "додепам", "dodep_num"]
        ]:
        top = nom[0]()
        res += f"Топ по {nom[1]}:\n"
        if top is None:
            res += "ашипка\n\n"
        else:
            res += "\n".join([f"{i + 1}. {top[i].name} - {getattr(top[i], nom[2])}" for i in range(len(top))]) + "\n\n"

    await msg.answer(res)


@dp.message(Command("menu"))
async def gay_menu(msg: types.Message):
    dv.set_date(msg.from_user.id)
    await msg.answer("Добро пожаловать, великий додепер", reply_markup=menu_keyboard)


@dp.message(F.text.lower() == "♣блекджек🃏")
async def gay_menu_blackjack(msg: types.Message):
    dv.set_date(msg.from_user.id)
    # await msg.answer("Добро пожаловать в блекджек", reply_markup=menu_keyboard)
    await msg.answer("Временно не работает. Here be blackjack.")


@dp.message(F.text.lower() == "🎰cлоты🎰")
async def gay_menu_slots(msg: types.Message):
    dv.set_date(msg.from_user.id)
    await msg.answer("Добро пожаловать в слоты", reply_markup=slots_keyboard)


@dp.message(F.text.lower() == "🔙назад🔙")
async def gay_back(msg: types.Message):
    dv.set_date(msg.from_user.id)
    await msg.answer("Добро пожаловать в меню", reply_markup=menu_keyboard)


@dp.message(F.text.lower() == "📛админ-панель❌")
async def gay_panel(msg: types.Message):
    dv.set_date(msg.from_user.id)
    if msg.from_user.id in config.ADMINS:
        await msg.answer("Админ панель включена", reply_markup=admin_keyboard)
    else:
        await msg.answer("ты недостоин")


async def main():
    print("starting bot..")

    dp.include_router(routes.slots.router)
    dp.include_router(routes.admins.router)
    dp.include_router(routes.blackjack.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())