from shop.gift import Gift
from db import db, dg

from aiogram import types


class PromoWelcome(Gift):
    def __init__(self):
        super().__init__(giftname="#welcome", cost=0, desc="добро пожаловать в Ракульцев-казино")

    def can_buy(self, id: int):
        return len(dg.get_typed_gifts("promo_welcome")) <= 10

    def shop_cap(self):
        return f"{self.giftname} ({self.cost}🪙)"

    async def open(self, msg: types.Message):
        if dg.has_gift(msg.from_user.id, "promo_welcome", show_gift=False):
            await msg.answer("Промокод уже активирован!")
            return
        db.add(msg.from_user.id, balance=150)
        dg.add_gift(msg.from_user.id, "promo_welcome", "#welcome", "", show_gift=False)
        await msg.answer("Промокод #welcome успешно применен!")
