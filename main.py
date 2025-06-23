# импорт всякой залупы
import asyncio

from aiogram import types, F
from aiogram.filters import Command, CommandObject, or_f

from db import db, dc, dg, utils
from tasks import credits_task
import routes.slots
import routes.admins
import routes.blackjack
import routes.shop
import routes.credits
from routes.keyboards import *
from messages import HELP, RULES
from middlewares.telegram import TGMiddleWare
from market.tasks import market_task
from config import ADMINS
from bot import bot, dp, scheduler

from datetime import datetime

import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="logs.log",
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s",
)

logging.getLogger('apscheduler').propagate = False
logging.getLogger('aiogram.event').propagate = False


@dp.message(Command("start"))
async def gay_start(msg: types.Message, command: CommandObject):
    """
    Регистрация пользователя (попытка зарегать)
    """
    args = None
    try:
        args = int(command.args)
    except (ValueError, TypeError):
        pass

    if utils.init_user(msg):
        if not args is None:
            user = db.get_user(args)
            if not user is None:
                db.add(user.id, 100)
                db.add(msg.from_user.id, balance=100)
        await msg.answer("Регистрация успешна!\n/menu - главное меню")
    else:
        await msg.answer("Регистрация не удалась, поплачь(\n/menu - главное меню")


@dp.message(or_f(F.text.lower() == "👥посетители👥", Command("visitors")))
async def gay_visitors(msg: types.Message):
    """
    Список пользователей, которые активничали последнюю минуту
    """
    vis = db.get_visit_list()
    await msg.answer(
        f"В казино: {len(vis)} человек\n"
        + "\n".join([f"{el.prefix}{el.name}" for el in vis])
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
    await msg.answer(utils.profile(msg.from_user.id))


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
    if db.get(msg.from_user.id, "balance") < 2:
        tdt = int(datetime.now().timestamp())
        last_dodep = db.get(msg.from_user.id, "dodep_date")
        timeout = 600 - 10 * db.get(msg.from_user.id, "balance")
        if tdt - last_dodep < timeout:
            await msg.answer(
                f"подождите {(timeout - tdt + last_dodep) // 60} минут {(timeout - tdt + last_dodep) % 60} секунд"
            )
        else:
            if (
                db.update(msg.from_user.id, balance=100)
                and db.add(msg.from_user.id, dodep_num=1)
                and db.update(msg.from_user.id, dodep_date=tdt)
            ):
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
        ["balance", "счету"],
        ["slots_num", "круткам"],
        ["blackjack_num", "играм в блэкджек"],
        ["dodep_num", "додепам"]
    ]:
        top = db.topn(5, nom[0])
        res += f"Топ по {nom[1]}:\n"
        if top is None:
            res += "ашипка\n\n"
        else:
            res += (
                "\n".join(
                    f"{i + 1}. {top[i].prefix}{top[i].name} - {getattr(top[i], nom[0])}"
                    for i in range(len(top))
                )
                + "\n\n"
            )
    await msg.answer(res)


@dp.message(Command("menu"))
async def gay_menu(msg: types.Message):
    await msg.answer("Добро пожаловать, великий додепер", reply_markup=menu_keyboard)


@dp.message(F.text.lower() == "♣блекджек🃏")
async def gay_menu_blackjack(msg: types.Message):
    await msg.answer("Вы дождались.\nДобро пожаловать в блэкджек", reply_markup=blackjack_keyboard)


@dp.message(F.text.lower() == "🎰cлоты🎰")
async def gay_menu_slots(msg: types.Message):
    await msg.answer("Добро пожаловать в слоты", reply_markup=slots_keyboard)


@dp.message(F.text.lower() == "🔙назад🔙")
async def gay_back(msg: types.Message):
    await msg.answer("Добро пожаловать в меню", reply_markup=menu_keyboard)


async def main():
    print("admins:", ADMINS)
    info = await bot.get_me()
    print("running bot:", info.username)
    print("starting bot..")

    dp.message.middleware(TGMiddleWare())

    dp.include_router(routes.admins.router)
    dp.include_router(routes.slots.router)
    dp.include_router(routes.blackjack.router)
    dp.include_router(routes.shop.router)
    dp.include_router(routes.credits.router)

    await credits_task()
    await market_task()
    scheduler.add_job(credits_task, "interval", seconds=15)
    scheduler.add_job(market_task, "interval", seconds=15)

    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
