from aiogram import Router, types, F, Bot
from aiogram.filters import Command

from games import slots
from db import db, dt, dv
from routes.admins import send_news
from games.slots import RULES

router = Router()

@router.message(F.text.lower() == "✨играть✨")
async def gay_spin(msg: types.Message):
    """
    Крутим жоска
    """
    dv.set_date(msg.from_user.id)
    msgs = slots.spin(db, dt, msg.from_user.id)
    for m in msgs:
        await msg.answer(m)
    if msgs[0] == slots.SECRET:
        await send_news(
            f"Пользователь {db.get_user(msg.from_user.id).name} выбил секретную комбинацию!!\n" + "прошлое комбо:" + slots.SECRET + "\n- КОМБИНАЦИЯ ИЗМЕНЕНА- ")
        slots.secret_regen()
        slots.secret_regen()
        slots.secret_regen()
    if msgs[0] == "🌈🌈🌈":
        await send_news(f"{db.get_user(msg.from_user.id).name} - absolute sigma!!")
    if msgs[0] == "💀💀💀":
        await send_news(f"{db.get_user(msg.from_user.id).name} проиграл семью в казино")

@router.message(Command("slots"))
async def gay_spinc(msg: types.Message):
    dv.set_date(msg.from_user.id)
    await gay_spin(msg)

@router.message(F.text.lower() == "🔥правила слотов🔥")
async def gay_slots_help(msg: types.Message):
    dv.set_date(msg.from_user.id)
    await msg.answer(RULES)