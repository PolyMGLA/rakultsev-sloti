from shop.gift import Gift
from db import db, dg
from market.data import data

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
    
    def description(self) -> str:
        return f"{self.desc} (курс: {data.hamster_course}🪙)"

    def shop_cap(self):
        return f"{self.giftname} ({self.cost}🪙)"

    async def open(self, msg: types.Message):
        user = db.get_user(msg.from_user.id)
        c = data.hamster_course

        if (c <= 2 or c >= 99) and not dg.has_gift(msg.from_user.id, "hamster_coin"):
            dg.add_gift(
                msg.from_user.id,
                "hamster_coin",
                "🐹HamsterCoin🐹",
                f"тап-тап-тап по хомяку (куплено по курсу {c})",
            )

        if db.add(user.id, balance=c):
            await msg.answer(
                f"Текущий курс монеты: {c}\nТекущий баланс: {user.balance + c}"
            )
        else:
            await msg.answer("Не получилось купить")
