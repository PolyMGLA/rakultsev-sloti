from aiogram import Router, types, F, Bot

from games import slots
from db.database import db, dt
from routes.admins import send_news

router = Router()

@router.message(F.text.lower() == "✨крутить✨")
async def gay_spin(msg: types.Message):
    """
    Крутим жоска
    """
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