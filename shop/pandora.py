from shop.gift import Gift
from games import slots
from db import db, dg

import random

from aiogram import types


async def open(msg: types.Message) -> str:
    user = db.get_user(msg.from_user.id)
    ch = random.randint(1, 101)
    if ch in range(1, 30) and db.add(user.id, prefix="🐔"):
        return "Выпало: 🐔курица🐔"
    if ch in range(30, 40) and db.add(user.id, balance=-10, lost_money=10):
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
        user = random.choice(users)
        num = random.randint(-50, 75)
        if db.add(user.id, balance=num, lost_money=(0 if num >= 0 else -num)):
            return f"Выдали случайному игроку {num}🪙"
        return "Ошибка %("
    if ch == 55:
        if not dg.has_gift(user.id, "pandora_lock"):
            dg.add_gift(
                user.id, "pandora_lock", "🔓Замок", "случайно отломан от ящика Пандоры"
            )
            return "Выпало: 🔓Замок"
        else:
            return "Выпало: ничего"
    if ch in range(56, 76):
        num = random.randint(-200, 150)
        if db.add(user.id, balance=num, lost_money=(0 if num >= 0 else -num)):
            return f"Выпало: {num}🪙"
        return "Ошибка %("
    if ch in range(76, 100):
        return "Выпало: ничего"
    if ch == 101:
        if db.add(user.id, balance=-5000, lost_money=5000):
            return "Выпало: -5000🪙 :)"
        return "Выпало: ничего"


class PandoraBox(Gift):
    def __init__(self):
        super().__init__(
            giftname="📦ящик пандоры📦", cost=125, desc="ящик со случайным содержимым"
        )

    def can_buy(self, id: int) -> bool:
        return True

    def shop_cap(self):
        return f"{self.giftname} ({self.cost}🪙)"

    async def open(self, msg: types.Message):
        if not dg.has_gift(msg.from_user.id, "pandora_box"):
            dg.add_gift(
                msg.from_user.id,
                "pandora_box",
                "📦Открытый ящик",
                "купил 📦ящик пандоры📦 в магазине",
            )

        await msg.answer(await open(msg))
