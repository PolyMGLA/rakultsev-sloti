from aiogram import Router, types, F
from aiogram.filters import Command, or_f

from games import slots
from db import db, dg
from games.slots import RULES

router = Router()


@router.message(or_f(F.text.lower() == "✨крутить✨", Command("slots")))
async def mh_spin(msg: types.Message):
    """
    Крутим жоска
    """
    bal = db.get(msg.from_user.id, "balance")
    if db.get_user(msg.from_user.id) == False:
        msgs = ["Вы еще не зарегистрированы!\n/start"]
    elif bal < 2:
        msgs = ["Недостаточно денег.\nБез додепа не разобраться\n /dodep"]
    else:
        msgs = await slots.spin(msg.from_user.id)
    for m in msgs:
        await msg.answer(m)


@router.message(F.text.lower() == "🔥правила слотов🔥")
async def mh_slots_help(msg: types.Message):
    await msg.answer(RULES)
