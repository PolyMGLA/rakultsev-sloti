from aiogram import Router, types, F
from aiogram.filters import Command, or_f

from games import slots
from db import db, dg
from games.slots import RULES
from middlewares.telegram import TGMiddleWare

router = Router()
router.message.middleware(TGMiddleWare())


@router.message(
    or_f(
        F.text.lower() == "✨крутить✨",
        F.text.lower() == "✨играть✨",
        Command("slots"),
    )
)
async def gay_spin(msg: types.Message):
    """
    Крутим жоска
    """
    bal = db.get_bal(msg.from_user.id)
    if db.get_user(msg.from_user.id) == False:
        msgs = ["Вы еще не зарегистрированы!\n/start"]
    elif bal < 2:
        msgs = ["Недостаточно денег.\nБез додепа не разобраться\n /dodep"]
    else:
        msgs = await slots.spin(db, dg, msg.from_user.id)
    for m in msgs:
        await msg.answer(m)
    


@router.message(F.text.lower() == "🔥правила слотов🔥")
async def gay_slots_help(msg: types.Message):
    await msg.answer(RULES)
