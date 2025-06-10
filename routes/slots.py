from aiogram import Router, types, F, Bot
from aiogram.filters import Command, or_f

from games import slots
from db import db, dt, dv, dg, utils
from routes.admins import send_news
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
    msgs = slots.spin(db, dt, msg.from_user.id)
    for m in msgs:
        await msg.answer(m)
    if msgs[0] == slots.SECRET:
        await send_news(
            f"Пользователь {db.get_user(msg.from_user.id).name} выбил секретную комбинацию!!\n"
            + "прошлое комбо:"
            + slots.SECRET
            + "\n- КОМБИНАЦИЯ ИЗМЕНЕНА- "
        )
        slots.secret_regen()
        slots.secret_regen()
        slots.secret_regen()
    if msgs[0] == "🌈🌈🌈":
        dg.add_gift(msg.from_user.id, "rainbow", "🌈Игрушечная радуга", "absolute sigma")
        await send_news(f"{db.get_user(msg.from_user.id).name} - absolute sigma!!")
    if msgs[0] == "💀💀💀":
        dg.add_gift(msg.from_user.id, "dead", "💀Игрушечный череп", "проиграл все")
        await send_news(f"{db.get_user(msg.from_user.id).name} проиграл семью в казино")


@router.message(F.text.lower() == "🔥правила слотов🔥")
async def gay_slots_help(msg: types.Message):
    await msg.answer(RULES)
