from shop.gift import Gift

from aiogram import types

class Air(Gift):
    def __init__(self):
        super().__init__(
            giftname = "🪙воздух🌪️",
            cost = 0,
            desc = "ящик со случайным содержимым"
        )
    
    def can_buy(self, id: int):
        return True
    
    def shop_cap(self):
        return f"{self.giftname} ({self.cost}🪙)"

    async def open(self, msg: types.Message):
        await msg.answer("Через секунду купленый воздух пропал.")