from aiogram import types, F, Router
from aiogram.filters import and_f
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import asyncio

from games import blackjack
from routes.keyboards import blackjack_keyboard, blackjack_game_keyboard, test_keyboard
from db import db
from middlewares.telegram import TGMiddleWare, TGAdminMiddleWare

router = Router()
router.message.middleware(TGMiddleWare())
router.message.middleware(TGAdminMiddleWare())
schet = 0
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
    elif action == "num_decr" and user_value > 1:
        await state.update_data(sum=user_value - 1)
        new_value = user_value - 1
    elif action == "num_decr10" and user_value > 11:
        await state.update_data(sum=user_value - 10)
        new_value = user_value - 10

    await update_num_text(callback.message, new_value)

    await callback.answer()


@router.callback_query(F.data == "start_game")
async def gay_start_game(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(BlackjackState.sum)
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
    

@router.message(and_f(F.text == "🃏взять карту", BlackjackState.sum))
async def gay_get_card(msg: types.Message, state: FSMContext):
    await blackjack.add_card(state, "my_cards")
    user_sum = (await state.get_data())["sum"]
    my_cards = (await state.get_data())['my_cards']
    dealer_cards = (await state.get_data())['dealer_cards']
    user_score = await blackjack.get_sum(state, "my_cards")
    await msg.answer(
        f"Ваша ставка: {user_sum}\n"
        + f"Ваши карты: {' '.join(my_cards)}\n"
        + f"Карты дилера: {' '.join(dealer_cards)}\n"
        + f"Ваш счет: {user_score}",
        reply_markup=blackjack_game_keyboard
        )
    if await blackjack.get_sum(state, "my_cards") == 21 and db.add(msg.from_user.id, balance=user_sum):
        await msg.answer("вы победили\n Ваш итоговый счет: 21", reply_markup=test_keyboard)
        return
    elif await blackjack.get_sum(state, "my_cards") > 21 and "🃏" in my_cards:
        for i in range(len(my_cards)):
            if my_cards[i] == "🃏":
                my_cards[i] = "1️⃣"
                user_score = await blackjack.get_sum(state, "my_cards")
                break
        await msg.answer("Ваше количество очков превысила 21\n Ваш туз превращается в единичку\n Новые Данные:")
        await msg.answer(
        f"Ваша ставка: {user_sum}\n"
        + f"Ваши карты: {' '.join(my_cards)}\n"
        + f"Карты дилера: {' '.join(dealer_cards)}\n"
        + f"Ваш счет: {user_score}",
        reply_markup=blackjack_game_keyboard
        )
        if await blackjack.get_sum(state, "my_cards") == 21 and db.add(msg.from_user.id, balance=user_sum):
            await msg.answer("вы победили\n Ваш итоговый счет: 21", reply_markup=test_keyboard)
            await state.clear()
            return
        return
    elif await blackjack.get_sum(state, "my_cards") > 21 and db.add(msg.from_user.id, balance=-user_sum):
        await msg.answer("Вы проиграли!", reply_markup=test_keyboard)
        await msg.answer("Ваш итоговый счет:", await blackjack.get_sum(state, "my_cards"))
        await state.clear()
    elif await blackjack.get_sum(state, "my_cards") == 87 and db.add(msg.from_user.id, balance=int(1.5 * user_sum)):
        await msg.answer("Блэкджек!", reply_markup=test_keyboard)
        await state.clear()


@router.message(F.text == "🛑стоп")
async def gay_stop(msg: types.Message, state: FSMContext):
    await blackjack.add_card(state, "my_cards")
    user_sum = (await state.get_data())["sum"]
    my_cards = (await state.get_data())['my_cards']
    dealer_cards = (await state.get_data())['dealer_cards']
    user_score = await blackjack.get_sum(state, "my_cards")
