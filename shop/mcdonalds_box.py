from shop.gift import Gift
from games.utils import randint
from routes.utils import send_news
from db import db

from aiogram import types


class MacDonaldsBox(Gift):
    def __init__(self):
        super().__init__(
            giftname="🍔Бокс из мака🍟",
            cost=101,
            desc="вернулся в РФ (все шутки про маму от Макса)",
        )

    def can_buy(self, id: int):
        return True

    def shop_cap(self):
        return f"{self.giftname} ({self.cost}🪙)"

    async def open(self, msg: types.Message):
        user = db.get_user(msg.from_user.id)
        ch = randint(1, 50)

        if ch == 1 and db.update(user.id, balance=user.balance - 2000):
            # await send_news(f"У пользователя {user.name} выпала мама из окнааа!!!! (бокс из мака)")
            await msg.answer("Выпало: проверь баланс")
        elif (
            2 <= ch <= 15
            and db.update(user.id, balance=user.balance - 30)
            and db.update(user.id, prefix="🐔")
        ):
            await msg.answer("Выпало: 🐔курица🐔 (не приготовленная? -30🪙)")
        elif 16 <= ch <= 24 and db.update(user.id, balance=user.balance + 30):
            await msg.answer("Выпало: 🍗курица🍗 (приготовленная? +30🪙)")
        elif 25 <= ch <= 30 and db.update(user.id, balance=user.balance + 180):
            await msg.answer("Выпало: 🍺пиво🍺 (+180🪙)")
        elif 31 <= ch <= 35 and db.update(user.id, balance=user.balance + 90):
            await msg.answer("Выпало: 🍔американский бургер🍔 (+90🪙)")
        elif 36 <= ch <= 40 and db.update(user.id, balance=user.balance - 50):
            await msg.answer("Выпало: 🍟картошка платная🍟 (-50🪙)")
        elif 41 <= ch <= 49 and db.update(user.id, balance=user.balance + 1):
            await msg.answer("Выпало: 🍦жидкое🍦 (+1🪙)")
        elif ch == 50:
            await msg.answer("Выпало: 🍼молочко🍼 (рано тебе в мак)")
        else:
            await msg.answer("ашипка")
