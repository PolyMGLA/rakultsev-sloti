from aiogram import Router, types, F

from routes.keyboards import shop_keyboard
from middlewares.telegram import TGMiddleWare, TGAdminMiddleWare

router = Router()
router.message.middleware(TGMiddleWare())
router.message.middleware(TGAdminMiddleWare())

@router.message(F.text.lower() == "💸магазин💸")
async def gay_shop(msg: types.Message):
    await msg.answer("Добро пожаловать в магазин💸", reply_markup=shop_keyboard)

@router.message(F.text.lower() == "🪙купить воздух🪙")
async def buy(msg: types.Message):
    await msg.answer(f"Куплено: воздух (использовать по назначению)\nЧерез секунду купленый воздух пропал.")
