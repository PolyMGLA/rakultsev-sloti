from shop.gift import Gift
from games.pandora import open
from db import dg

from aiogram import types

class PandoraBox(Gift):
    def __init__(self):
        super().__init__(
            giftname = "📦ящик пандоры📦",
            cost = 125,
            desc = "ящик со случайным содержимым"
        )

    def can_buy(self, id: int) -> bool:
        return True
    
    def shop_cap(self):
        return f"{self.giftname} ({self.cost}🪙)"

    async def open(self, msg: types.Message):
        await msg.answer(f"Куплено: {self.giftname}")
        if not dg.has_gift(msg.from_user.id, "pandora_box"):
            dg.add_gift(msg.from_user.id, "pandora_box", "📦Открытый ящик", "купил 📦ящик пандоры📦 в магазине")
        
        await msg.answer(await open(msg))