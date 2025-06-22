from shop.gift import Gift
from db import db, dg

from aiogram import types


class PromoEmpty(Gift):
    def __init__(self):
        super().__init__(giftname="#", cost=0, desc="ты дурачок?")

    def can_buy(self, id: int):
        return True

    def shop_cap(self):
        return f"{self.giftname} ({self.cost}🪙)"

    async def open(self, msg: types.Message):
        if db.add(msg.from_user.id, balance=-50):
            await msg.answer("Промокод не может быть пустым. Вот тебе -50🪙 за это")
