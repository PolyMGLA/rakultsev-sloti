from shop.gift import Gift
from db import db
from bot import bot

from aiogram import types

import logging

logger = logging.getLogger(__name__)

import random


class Shotgun(Gift):
    def __init__(self):
        super().__init__(
            giftname="🔫пистолет",
            cost=105,
            desc="снять у себя и случайного игрока 105🪙",
        )

    def can_buy(self, id: int):
        return True

    def shop_cap(self):
        return f"{self.giftname} ({self.cost}🪙)"

    async def open(self, msg: types.Message):
        randu = random.choice(db.users_list())
        user = db.get_user(msg.from_user.id)
        if random.randint(1, 100) <= 85 and randu.id != msg.from_user.id:
            if db.add(randu.id, balance=-105):
                logger.info(
                    f"{user.name}({msg.from_user.id}) застрелил {randu.name}({randu.id})"
                )
                await msg.answer(
                    f"Вы застрелили: {randu.name}\nВаш баланс: {db.get(msg.from_user.id, 'balance')}\nЕго баланс: {db.get(randu.id, 'balance')}"
                )
                await bot.send_message(
                    randu.id,
                    f"Вас застрелил: {user.name}\nЕго баланс: {db.get(msg.from_user.id, 'balance')}\nВаш баланс: {db.get(randu.id, 'balance')}",
                )
            else:
                await msg.answer("ашипка")
        else:
            if db.add(msg.from_user.id, balance=-105):
                logger.info(f"{user.name}({msg.from_user.id}) застрелился")
                await msg.answer(
                    f"Вы случайно застрелили себя.\nВаш баланс: {db.get(msg.from_user.id, 'balance')}"
                )
            else:
                await msg.answer("ашипка")
