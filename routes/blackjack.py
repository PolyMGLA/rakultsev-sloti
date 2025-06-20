from aiogram import types, F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from games import blackjack
from routes.keyboards import blackjack_keyboard, blackjack_game_keyboard, test_keyboard
from db import db
from middlewares.telegram import TGMiddleWare, TGAdminMiddleWare

router = Router()
router.message.middleware(TGMiddleWare())
router.message.middleware(TGAdminMiddleWare())

class BlackjackState(StatesGroup):
    sum = State()
    cards_arr = State()
    my_cards = State()
    dealer_cards = State()


def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="-10", callback_data="num_decr10"),
            types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
            types.InlineKeyboardButton(text="+1", callback_data="num_incr"),
            types.InlineKeyboardButton(text="+10", callback_data="num_incr10"),
        ],
        [types.InlineKeyboardButton(text="Подтвердить", callback_data="start_game")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def update_num_text(message: types.Message, new_value: int):
    await message.edit_text(f"Укажите ставку: {new_value}", reply_markup=get_keyboard())


@router.message(F.text.lower() == "✨сосать✨")
async def gay_stavka(message: types.Message, state: FSMContext):
    await state.update_data(sum=2)
    await message.answer("Укажите ставку: 2", reply_markup=get_keyboard())


@router.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery, state: FSMContext):
    user_value = (await state.get_data())["sum"]
    action = callback.data
    if action == "num_incr":
        await state.update_data(sum=user_value + 1)
        new_value = user_value + 1
    elif action == "num_incr10":
        await state.update_data(sum=user_value + 10)
        new_value = user_value + 10
    elif action == "num_decr" and user_value > 2:
        await state.update_data(sum=user_value - 1)
        new_value = user_value - 1
    elif action == "num_decr10" and user_value > 11:
        await state.update_data(sum=user_value - 10)
        new_value = user_value - 10

    await update_num_text(callback.message, new_value)

    await callback.answer()


@router.callback_query(F.data == "start_game")
async def gay_start_game(callback: types.CallbackQuery, state: FSMContext):
    user_value = (await state.get_data())["sum"]
    cards = blackjack.shuffle()
    await state.update_data(cards_arr=cards, my_cards=[], dealer_cards=[])
    await blackjack.add_card(state, "my_cards")
    await blackjack.add_card(state, "my_cards")
    await blackjack.add_card(state, "dealer_cards")
    await blackjack.add_card(state, "dealer_cards")
    my_cards = (await state.get_data())['my_cards']
    dealer_cards = (await state.get_data())['dealer_cards']

    await callback.message.edit_text(
        f"Ваша ставка: {user_value}\n"
        + f"Ваши карты: {' '.join(my_cards)}\n"
        + f"Карты дилера: 🎁 {' '.join(dealer_cards[1:])}"
        )
    await callback.message.answer("Выберите действие", reply_markup=blackjack_game_keyboard)
    

@router.message(F.text == "🃏взять карту")
async def gay_get_card(msg: types.Message, state: FSMContext):
    await blackjack.add_card(state, "my_cards")
    user_sum = (await state.get_data())["sum"]
    my_cards = (await state.get_data())['my_cards']
    dealer_cards = (await state.get_data())['dealer_cards']
    await msg.answer(
        f"Ваша ставка: {user_sum}\n"
        + f"Ваши карты: {' '.join(my_cards)}\n"
        + f"Карты дилера: {' '.join(dealer_cards)}",
        reply_markup=blackjack_game_keyboard
        )
    
    if await blackjack.get_sum(state, "my_cards") > 21 \
        and "🃏" not in my_cards \
        and db.update_bal(
            msg.from_user.id,
            db.get_bal(msg.from_user.id) - user_sum
            ):
        await msg.answer("Вы проебали!", reply_markup=test_keyboard)