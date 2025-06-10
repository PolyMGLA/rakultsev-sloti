from games import utils, slots
from db import db, dt, dg
from db.database import CasinoUsers

from aiogram import types

async def open(user: CasinoUsers, msg: types.Message) -> str:
    ch = utils.randint(1, 100)
    if ch in range(1, 30):
        return "Выпало: 🐔курица🐔"
    if ch in range(30, 40) and db.update_bal(user.id, user.balance - 10):
        return "Выпало: 🦆утка🦆. -10🪙"
    if ch in range(40, 45):
        for i in range(10):
            for el in await slots.spin(db, dg, user.id):
                await msg.answer(el)
        return "Выпало: 🐎лошадь🐎. Крутим слоты."
    if ch in range(45, 55):
        users = db.users_list()
        if users is None:
            return "Ошибка %("
        user = utils.choice(users)
        num = utils.randint(-20, 20)
        if db.update_bal(user.id, user.balance + num):
            return f"Выдали случайному игроку {num}🪙"
        return "Ошибка %("
    if ch == 55:
        if not dg.has_gift(user.id, "pandora_lock"):
            dg.add_gift(user.id, "pandora_lock", "🔓Замок", "случайно отломан от ящика Пандоры")
            return "Выпало: 🔓Замок"
        else:
            return "Выпало: ничего"
    if ch in range(56, 76):
        num = utils.randint(-200, 200)
        if db.update_bal(user.id, user.balance + num):
            return f"Выпало: {num}🪙"
        return "Ошибка %("
    if ch in range(76, 100):
        return "Выпало: ничего"
    if ch == 101:
        if db.update_bal(user.id, user.balance - 5000):
            return "Выпало: -5000🪙 :)"
        return "Выпало: ничего"
