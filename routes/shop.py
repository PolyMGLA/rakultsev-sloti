from aiogram import Router, types, F
from aiogram.filters import or_f, Command

from messages import DONATE
from middlewares.telegram import TGMiddleWare, TGAdminMiddleWare
from db import db, dg
from games import pandora
from shop import gifts

router = Router()
router.message.middleware(TGMiddleWare())

SHOP_LIST = """- Товары в магазине -\n""" + "\n".join([f"{i}. {el.giftname} - {el.desc}" for i, el in enumerate(gifts, 1)])


def get_shop_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="💲мега ласт деп💲"),
                types.KeyboardButton(text="🛍️Описание товаров🛍️")
            ],
            [
                types.KeyboardButton(text=gifts[0].shop_cap()),
                types.KeyboardButton(text=gifts[1].shop_cap()),
            ],
            [
                types.KeyboardButton(text=gifts[2].shop_cap()),
            ],
            [types.KeyboardButton(text="🔙Назад🔙")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите что хотите сделать",
    )


@router.message(or_f(F.text.lower() == "💸магазин💸", Command("shop")))
async def gay_shop(msg: types.Message):
    shop_keyboard = get_shop_keyboard()

    await msg.answer("Добро пожаловать в магазин💸", reply_markup=shop_keyboard)


@router.message(F.text.lower() == "🛍️описание товаров🛍️")
async def gay_shop_list(msg: types.Message):
    await msg.answer(SHOP_LIST)


for gift in gifts:
    @router.message(F.text == gift.shop_cap())
    async def gay_gift(msg: types.Message, gift=gift):
        user = db.get_user(msg.from_user.id)
        if gift.can_buy(msg.from_user.id):
            if user.balance >= gift.cost \
                and db.update_bal(msg.from_user.id, user.balance - gift.cost):
                await gift.open(msg)
            else:
                await msg.answer("недостаточно денег!")
        else:
            await msg.answer("все распродано.")


@router.message(F.text.lower() == "💸донат админам💸")
async def gay_donate(msg: types.Message):
    await msg.answer(DONATE)

