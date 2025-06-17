from shop.gift import Gift
from games.utils import randint
from db import db

from aiogram import types

class HamsterCoin(Gift):
    def __init__(self):
        super().__init__(
            giftname = "🐹HamsterCoin🐹",
            cost = 100,
            desc = "криптовалюта HamsterCoin из коллаборации"
        )
    
    def can_buy(self, id: int):
        return True
    
    def shop_cap(self):
        return f"{self.giftname} ({self.cost}🪙)"

    async def open(self, msg: types.Message):
        user = db.get_user(msg.from_user.id)
        c = randint(1, 50)
        if db.update_bal(user.id, user.balance + c):
            await msg.answer(f"Текущий курс монеты: {c}\nТекущий баланс: {user.balance + c}")
        else:
            await msg.answer("Не получилось купить")