                                                                    #импорт всякой залупы
import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, or_f

from db import db, dt, dv, utils
import routes.slots
import routes.admins
import routes.blackjack
from routes.keyboards import *
import config
from messages import HELP, RULES
from middlewares.telegram import TGMiddleWare

from datetime import datetime

from bot import bot, dp

"""
TODO:
Блэкджек
Магазин
Кредиты в магазине (берешь кредит на несколько дней/недель, по окончанию срока должен выплатить сумму кредита, иначе через 3 дня на счет начислится минус с большим коэффициентом)
"""


@dp.message(Command("start"))
async def gay_start(msg: types.Message):
    """
    Регистрация пользователя (попытка зарегать)
    """
    
    if utils.init_user(msg):
        await msg.answer("Регистрация успешна!\n/menu - главное меню")
    else:
        await msg.answer("Регистрация не удалась, поплачь(\n/menu - главное меню")


@dp.message(or_f(F.text.lower() == "👥посетители👥", Command("visitors")))
async def gay_visitors(msg: types.Message):
    """
    Список пользователей, которые активничали последнюю минуту
    """
    vis = dv.get_list()
    await msg.answer(
        f"В казино: {len(vis)} человек\n" \
        + "\n".join([f"{el.user.name}" for el in vis])
    )


@dp.message(or_f(F.text.lower() == "🆘помощь🆘", Command("help")))
async def gay_help(msg: types.Message):
    """
    Собсна текст помощи утопающим
    """
    await msg.answer(HELP)


@dp.message(or_f(F.text.lower() == "👾профиль👾", Command("profile")))
async def gay_profile(msg: types.Message):
    """
    Инфо о профиле пользователя
    """
    user = db.get_user(msg.from_user.id)
    if user is None or user == False:
        await msg.answer("Вы не зарегистрированы!\n/start")
    else:
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

    P.s. Удалено из меню
    """
    await msg.answer(RULES)


@dp.message(or_f(F.text.lower() == "💲мега ласт деп💲", Command("dodep")))
async def gay_dodep(msg: types.Message):
    """
    Функция для пополнения баланса на аккаунте (собственно говоря, додеп)
    """
    user = db.get_user(msg.from_user.id)
    if user.balance < 2:

        tdt = int(datetime.now().timestamp())
        last_dodep = dt.get_date(msg.from_user.id).date
        timeout = 600 - 10 * db.get_bal(msg.from_user.id)
        if tdt - last_dodep < timeout:
            await msg.answer(f"подождите {(timeout - tdt + last_dodep) // 60} минут {(timeout - tdt + last_dodep) % 60} секунд")
        else:
            if db.update_bal(msg.from_user.id, 100) and db.add_dodep(msg.from_user.id) and dt.set_date(msg.from_user.id, tdt):
                await msg.answer("додеп прошел")
            else:
                await msg.answer("додеп не прошел")
    else:
        await msg.answer("вы слишком богатые")


@dp.message(or_f(F.text.lower() == "🔝топ казино🎰", Command("top")))
async def gay_top(msg: types.Message):
    """
    Топ казино по балансу, круткам слотов и додепам
    """
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
    await msg.answer("Добро пожаловать, великий додепер", reply_markup=menu_keyboard)


@dp.message(F.text.lower() == "♣блекджек🃏")
async def gay_menu_blackjack(msg: types.Message):
    # await msg.answer("Добро пожаловать в блекджек", reply_markup=menu_keyboard)
    await msg.answer("Временно не работает. Here be blackjack.")


@dp.message(F.text.lower() == "🎰cлоты🎰")
async def gay_menu_slots(msg: types.Message):
    await msg.answer("Добро пожаловать в слоты", reply_markup=slots_keyboard)


@dp.message(F.text.lower() == "🔙назад🔙")
async def gay_back(msg: types.Message):
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

    dp.message.middleware(TGMiddleWare())

    dp.include_router(routes.slots.router)
    dp.include_router(routes.admins.router)
    dp.include_router(routes.blackjack.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())