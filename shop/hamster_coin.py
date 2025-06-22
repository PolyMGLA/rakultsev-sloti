from shop.gift import Gift
from db import db, dg

import random

from aiogram import types


class HamsterCoin(Gift):
    def __init__(self):
        super().__init__(
            giftname="🐹HamsterCoin🐹",
            cost=99,
            desc="криптовалюта HamsterCoin из коллаборации",
        )

    def can_buy(self, id: int):
        return True

    def shop_cap(self):
        return f"{self.giftname} ({self.cost}🪙)"

    async def open(self, msg: types.Message):
        user = db.get_user(msg.from_user.id)
        c = random.randint(1, 50)

        if c <= 5 and not dg.has_gift(msg.from_user.id, "hamster_coin"):
            dg.add_gift(
                msg.from_user.id,
                "hamster_coin",
                "🐹HamsterCoin🐹",
                f"тап-тап-тап по хомяку (куплено по курсу {c})",
            )

        if db.update(user.id, balance=user.balance + c):
            await msg.answer(
                f"Текущий курс монеты: {c}\nТекущий баланс: {user.balance + c}"
            )
        else:
            await msg.answer("Не получилось купить")
