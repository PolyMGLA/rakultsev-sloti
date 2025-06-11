from aiogram import Router, types, F
from aiogram.filters import or_f, Command

from messages import DONATE
from middlewares.telegram import TGMiddleWare, TGAdminMiddleWare
from db import db, dg
from games import pandora

router = Router()
router.message.middleware(TGMiddleWare())


SHOP_LIST = """
- Товары в магазине -
1. воздух🌪️ - просто воздух. Буквально ничего не дает
2. кубок лудомана🏆 - подарок в профиль. лимитированная коллекция из 5 экземпляров.
3. 📦ящик пандоры📦 - ящик со случайным содержимым
"""


def get_shop_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="💲мега ласт деп💲"),
                types.KeyboardButton(text="🛍️Описание товаров🛍️")
            ],
            [
                types.KeyboardButton(text="🪙воздух🌪️ (0🪙)"),
                # types.KeyboardButton(text=f"🪙кубок лудомана🏆 (150🪙, Limited {5 - dg.count_type("lud_cup")}/5)")
                types.KeyboardButton(text="📦Ящик пандоры📦 (125🪙)"),
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


@router.message(F.text.lower() == "🪙воздух🌪️ (0🪙)")
async def gay_buy_air(msg: types.Message):
    await msg.answer(
        f"Куплено: воздух (использовать по назначению)\nЧерез секунду купленый воздух пропал."
    )


@router.message(F.text.lower().startswith("🪙кубок лудомана🏆 (150🪙, limited"))
async def gay_buy_cup(msg: types.Message):
    user = db.get_user(msg.from_user.id)
    if dg.count_type("lud_cup") + 1 <= 5:
        if not dg.has_gift(user.id, "lud_cup"):
            if user.balance >= 150 and db.update_bal(user.id, user.balance - 150):
                dg.add_gift(msg.from_user.id, "lud_cup", "кубок лудомана🏆", "куплено в лимитированной коллекции")
                await msg.answer("Куплено: кубок лудомана🏆")
            else:
                await msg.answer("недостаточно денег!")
        else:
            await msg.answer("уже куплено")
    else:
        await msg.answer("Все распродано.")


@router.message(F.text.lower() == "📦ящик пандоры📦 (125🪙)")
async def gay_pandora_box(msg: types.Message):
    user = db.get_user(msg.from_user.id)
    if db.get_bal(msg.from_user.id) >= 125 and db.update_bal(user.id, db.get_bal(msg.from_user.id) - 125):
        await msg.answer("Куплено: 📦ящик пандоры📦")
        if not dg.has_gift(user.id, "pandora_box"):
            dg.add_gift(user.id, "pandora_box", "📦Открытый ящик", "купил 📦ящик пандоры📦 в магазине")
        await msg.answer(await pandora.open(msg))
    else:
        await msg.answer("недостаточно денег!")


@router.message(F.text.lower() == "💸донат админам💸")
async def gay_donate(msg: types.Message):
    await msg.answer(DONATE)

