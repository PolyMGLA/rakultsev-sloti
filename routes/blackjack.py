from aiogram import types, F, Router
from aiogram.filters import and_f, or_f, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import asyncio

from games import blackjack
from routes.keyboards import blackjack_keyboard, blackjack_game_keyboard
from db import db
from middlewares.telegram import TGMiddleWare

router = Router()
router.message.middleware(TGMiddleWare())


class BlackjackState(StatesGroup):
    sum = State()
    cards_arr = State()
    my_cards = State()
    dealer_cards = State()


@router.message(F.text.lower() == "🔥правила блэкджека🔥")
async def blackjack_rules(msg: types.Message):
    await msg.answer(blackjack.RULES)


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


@router.message(or_f(F.text.lower() == "✨играть✨", Command("blackjack")))
async def gay_stavka(msg: types.Message, state: FSMContext):
    db.add(msg.from_user.id, blackjack_num=1)
    await state.update_data(sum=2)
    await msg.answer("Укажите ставку: 2", reply_markup=get_keyboard())


@router.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery, state: FSMContext):
    user_bal = db.get(callback.from_user.id, "balance")
    user_value = (await state.get_data())["sum"]
    action = callback.data
    if action == "num_incr":
        user_value += 1
    elif action == "num_incr10":
        user_value += 10
    elif action == "num_decr":
        user_value -= 1
    elif action == "num_decr10":
        user_value -= 10

    if user_value <= 0:
        await callback.answer("Вы не можете поставить отрицательную или нулевую сумму")
    elif user_value <= user_bal:
        await state.update_data(sum=user_value)
        await update_num_text(callback.message, user_value)
        await callback.answer()
    else:
        await callback.answer("Недостаточно денег")


async def send_blackjack_status(
        msg: types.Message,
        user_sum: int,
        my_cards: list[str],
        dealer_cards: list[str],
        user_score: int,
        dealer_score: int
        ):
    return await msg.answer(
        f"Ваша ставка: {user_sum}\n"
        + f"Ваши карты: {' '.join(my_cards)}\n"
        + f"Карты дилера: {' '.join(dealer_cards)}\n"
        + f"Ваш счет: {user_score}\n"
        + f"Счет Дилера: {dealer_score}",
        reply_markup=blackjack_game_keyboard
        )


async def edit_blackjack_status(
        msg: types.Message,
        user_sum: int,
        my_cards: list[str],
        dealer_cards: list[str],
        user_score: int,
        dealer_score: int
        ):
    new_text = (f"Ваша ставка: {user_sum}\n"
        + f"Ваши карты: {' '.join(my_cards)}\n"
        + f"Карты дилера: {' '.join(dealer_cards)}\n"
        + f"Ваш счет: {user_score}\n"
        + f"Счет Дилера: {dealer_score}")

    if new_text == msg.text:
        return msg

    return await msg.edit_text(new_text)


@router.callback_query(F.data == "start_game")
async def gay_start_game(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(BlackjackState.sum)
    user_value = (await state.get_data())["sum"]
    
    await state.update_data(cards_arr=blackjack.shuffle(), my_cards=[], dealer_cards=[])
    await blackjack.add_card(state, "my_cards")
    await blackjack.add_card(state, "my_cards")
    await blackjack.add_card(state, "dealer_cards")
    await blackjack.add_card(state, "dealer_cards")

    my_cards = (await state.get_data())['my_cards']
    dealer_cards = (await state.get_data())['dealer_cards']
    user_sum = (await state.get_data())["sum"]
    user_score = await blackjack.get_sum(state, "my_cards")

    await callback.message.edit_text(
        f"Ваша ставка: {user_value}\n"
        + f"Ваши карты: {' '.join(my_cards)}\n"
        + f"Карты дилера: 🎁 {' '.join(dealer_cards[1:])}\n"
        + f"Ваш счет: {user_score}\n"
        )

    if await blackjack.get_sum(state, "my_cards") == 87 and db.add(callback.from_user.id, balance=int(1.5 * user_sum)):
        await callback.message.answer("Блэкджек!", reply_markup=blackjack_keyboard)
        await state.clear()
    else:
        await callback.message.answer("Выберите действие", reply_markup=blackjack_game_keyboard)


@router.message(and_f(F.text == "🃏взять карту", BlackjackState.sum))
async def gay_get_card(msg: types.Message, state: FSMContext):
    await blackjack.add_card(state, "my_cards")
    user_sum: int = (await state.get_data())["sum"]
    my_cards: list[str] = (await state.get_data())['my_cards']
    dealer_cards: list[str] = (await state.get_data())['dealer_cards']
    user_score: int = await blackjack.get_sum(state, "my_cards")
    dealer_score: int = await blackjack.get_sum(state, "dealer_cards")

    await send_blackjack_status(msg, user_sum, my_cards, dealer_cards, user_score, dealer_score)
    
    if user_score == 21 and db.add(msg.from_user.id, balance=user_sum):
        await msg.answer("вы победили\n Ваш итоговый счет: 21", reply_markup=blackjack_keyboard)
        await state.clear()
    elif await blackjack.get_sum(state, "my_cards") > 21 and "🃏" in my_cards:
        my_cards[my_cards.index("🃏")] = "1️⃣"
        user_score -= 10
        await msg.answer("Ваше количество очков превысила 21\n Ваш туз превращается в единичку\n Новые Данные:")
        await send_blackjack_status(msg, user_sum, my_cards, dealer_cards, user_score, dealer_score)

        if user_score == 21 and db.add(msg.from_user.id, balance=user_sum):
            await msg.answer("Вы победили\n Ваш итоговый счет: 21", reply_markup=blackjack_keyboard)
            await state.clear()
    elif user_score > 21 and db.add(msg.from_user.id, balance=-user_sum, lost_money=user_sum):
        await msg.answer(f"Вы проиграли!\nВаш итоговый счет: {await blackjack.get_sum(state, 'my_cards')}", reply_markup=blackjack_keyboard)
        await state.clear()
    elif user_score == 87 and db.add(msg.from_user.id, balance=int(1.5 * user_sum)):
        await msg.answer("Блэкджек!", reply_markup=blackjack_keyboard)
        await state.clear()
    elif dealer_score == 87 and db.add(msg.from_user.id, balance=-user_sum, lost_money=user_sum):
        await msg.answer("У дилера Блэкджек!", reply_markup=blackjack_keyboard)
        await state.clear()
    elif dealer_score > 21 and "🃏" in dealer_cards:
        dealer_cards[dealer_cards.index("🃏")] = "1️⃣"
        dealer_score -= 10
        await msg.answer("Количество очков дилера превысило 21\nТуз Дилера превращается в единичку\nНовые Данные:")
        await send_blackjack_status(msg, user_sum, my_cards, dealer_cards, user_score, dealer_score)

        if dealer_score == 21 and db.add(msg.from_user.id, balance=-user_sum, lost_money=user_sum):
            await msg.answer("Вы проиграли\nДилер набрал 21 очко", reply_markup=blackjack_keyboard)
            await state.clear()


@router.message(and_f(F.text == "🛑стоп", BlackjackState.sum))
async def gay_stop(msg: types.Message, state: FSMContext):
    user_sum: int = (await state.get_data())["sum"]
    my_cards: list[str] = (await state.get_data())['my_cards']
    dealer_cards: list[str] = (await state.get_data())['dealer_cards']
    user_score: int = await blackjack.get_sum(state, "my_cards")
    dealer_score: int = await blackjack.get_sum(state, "dealer_cards")

    await send_blackjack_status(msg, user_sum, my_cards, dealer_cards, user_score, dealer_score)

    while dealer_score <= 17:
        await blackjack.add_card(state, "dealer_cards")

        dealer_cards = (await state.get_data())['dealer_cards']
        dealer_score = await blackjack.get_sum(state, "dealer_cards")

        await send_blackjack_status(msg, user_sum, my_cards, dealer_cards, user_score, dealer_score)

        if dealer_score > 21 and "🃏" in dealer_cards:
            dealer_cards[dealer_cards.index("🃏")] = "1️⃣"
            dealer_score -= 10
            await msg.answer("Количество очков дилера превысило 21\nТуз Дилера превращается в единичку\nНовые Данные:")
            await send_blackjack_status(msg, user_sum, my_cards, dealer_cards, user_score, dealer_score)

            if dealer_score == 21 and db.add(msg.from_user.id, balance=-user_sum, lost_money=user_sum):
                await msg.answer("Вы проиграли\nДилер набрал 21 очко", reply_markup=blackjack_keyboard)
                await state.clear()
                return

        await asyncio.sleep(0.3)
    if dealer_score == user_score:
        await msg.answer("Ничья", reply_markup=blackjack_keyboard)
        await state.clear()
    elif dealer_score == 21 and db.add(msg.from_user.id, balance=-user_sum, lost_money=user_sum):
        await msg.answer("Вы проиграли\nДилер набрал 21 очко!", reply_markup=blackjack_keyboard)
        await state.clear()
    elif dealer_score == 87 and db.add(msg.from_user.id, balance=-user_sum, lost_money=user_sum):
        await msg.answer("У дилера Блэкджек!", reply_markup=blackjack_keyboard)
        await state.clear()
    elif dealer_score > 21 and db.add(msg.from_user.id, balance=user_sum):
        await msg.answer(f"Вы выиграли!\nСчет дилера превысил 21\nВаш итоговый счет: {await blackjack.get_sum(state, 'my_cards')}", reply_markup=blackjack_keyboard)
        await state.clear()
    elif dealer_score > user_score and db.add(msg.from_user.id, balance=-user_sum, lost_money=user_sum):
        await msg.answer(f"Вы проиграли!\nВаш счет:{user_score}\nСчет Дилера: {dealer_score}", reply_markup=blackjack_keyboard)
        await state.clear()
    elif dealer_score < user_score and db.add(msg.from_user.id, balance=user_sum):
        await msg.answer(f"Вы выиграли!\nВаш счет:{user_score}\nСчет Дилера: {dealer_score}", reply_markup=blackjack_keyboard)
        await state.clear()
    else:
        await msg.answer("ашипка")
        await state.clear()

@router.message(and_f(F.text == "🏳️сдаться", BlackjackState.sum))
async def gay_exit(msg: types.Message, state: FSMContext):
    user_sum: int = (await state.get_data())["sum"]

    if db.add(msg.from_user.id, balance=-(user_sum // 2), lost_money=user_sum // 2):
        await msg.answer("Вы сдались, вам возвращена половина ставки", reply_markup=blackjack_keyboard)
        await state.clear()
    else:
        await msg.answer("ашипка")
        await state.clear()
