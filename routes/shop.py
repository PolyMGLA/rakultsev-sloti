from aiogram import Router, types, F
from aiogram.filters import or_f, Command

from messages import DONATE
from routes.keyboards import shop_keyboard
from middlewares.telegram import TGMiddleWare, TGAdminMiddleWare
from db import db, dg

router = Router()
router.message.middleware(TGMiddleWare())


@router.message(or_f(F.text.lower() == "💸магазин💸", Command("shop")))
async def gay_shop(msg: types.Message):
    await msg.answer("Добро пожаловать в магазин💸", reply_markup=shop_keyboard)


@router.message(F.text.lower() == "🪙воздух🌪️ (0🪙)")
async def gay_buy_air(msg: types.Message):
    await msg.answer(
        f"Куплено: воздух (использовать по назначению)\nЧерез секунду купленый воздух пропал."
    )


@router.message(F.text.lower() == "🪙кубок лудомана🏆 (150🪙, limited)")
async def gay_buy_cup(msg: types.Message):
    user = db.get_user(msg.from_user.id)
    if dg.count_type("lud_cup") + 1 <= 5:
        if user.balance >= 150 and db.update_bal(user.id, user.balance - 150):
            dg.add_gift(msg.from_user.id, "lud_cup", "кубок лудомана🏆", "куплено в лимитированной коллекции")
            await msg.answer("Куплено: кубок лудомана🏆")
        else:
            await msg.answer("недостаточно денег")
    else:
        await msg.answer("Все распродано.")


@router.message(F.text.lower() == "💸донат админам💸")
async def gay_donate(msg: types.Message):
    await msg.answer(DONATE)

