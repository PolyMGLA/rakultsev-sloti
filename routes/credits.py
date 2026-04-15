from aiogram import Router, types, F
from aiogram.filters import Command, or_f
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from datetime import datetime

from db import db, dc

router = Router()


def get_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📜пользовательское соглашение📜")],
            [
                types.KeyboardButton(text="175🪙/20% в час/1 день"),
            ],
            [
                types.KeyboardButton(text="💳мои кредиты💰"),
                types.KeyboardButton(text="💵погасить кредит💵"),
            ],
            [types.KeyboardButton(text="💸магазин💸")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите что хотите сделать",
    )


class PayForm(StatesGroup):
    credit = State()
    pay = State()


@router.message(F.text.lower() == "💰кредиты💳")
async def mh_credits(msg: types.Message):
    await msg.answer(
        "Кредиты. Не забудьте прочитать пользовательское соглашение!",
        reply_markup=get_keyboard(),
    )


@router.message(F.text.lower() == "📜пользовательское соглашение📜")
async def mh_doc(msg: types.Message):
    doc = types.FSInputFile("./doc/Пользовательское соглашение.docx")
    await msg.answer_document(doc, caption="Настоящее пользовательское соглашение📜")


@router.message(or_f(F.text.lower() == "💳мои кредиты💰", Command("my_credits")))
async def mh_my_credits(msg: types.Message):
    credlist = dc.get_user_credits(msg.from_user.id)
    if len(credlist) == 0:
        await msg.answer("Кредитов нет!")

    for cred in credlist:
        await msg.answer(
            f"Кредит №{cred.credit_id} на {cred.sum}🪙 под {cred.perc}% в день. Погасить до {datetime.fromtimestamp(cred.last_date).strftime('%d/%m/%Y, %H:%M:%S')}"
        )


@router.message(F.text.lower() == "175🪙/20% в час/1 день")
async def mh_credit1(msg: types.Message):
    user = db.get_user(msg.from_user.id)
    credlist = dc.get_user_credits(msg.from_user.id)
    if len(credlist) >= 5:
        await msg.answer("слишком много кредитов взято")
        return

    now = datetime.now().timestamp()
    if dc.add_credit(user.id, 175, 15, now, now + 86400, cred_period=3600) and db.add(
        user.id, balance=175
    ):
        await msg.answer("Кредит успешно взят! Не забудьте отдать его в срок..")
    else:
        await msg.answer("ашипка")


@router.message(or_f(F.text.lower() == "💵погасить кредит💵", Command("pay")))
async def credit_pay1(msg: types.Message, state: FSMContext):
    credlist = dc.get_user_credits(msg.from_user.id)
    if len(credlist) == 0:
        await msg.answer("Кредитов нет!")
        return

    for cred in credlist:
        await msg.answer(
            f"Кредит №{cred.credit_id} на {cred.sum}🪙 под {cred.perc}% в день. Погасить до {datetime.fromtimestamp(cred.last_date).strftime('%d/%m/%Y, %H:%M:%S')}"
        )
    await msg.answer("Выберите номер кредита, который хотите погасить!")
    await state.set_state(PayForm.credit)


@router.message(PayForm.credit)
async def credit_pay2(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        credit_id = int(msg.text)
        credlist = dc.get_user_credits(msg.from_user.id)
        for cred in credlist:
            if cred.credit_id == int(msg.text):
                await state.update_data(credit_id=credit_id)
                await state.set_state(PayForm.pay)
                await msg.answer("Введите сумму, которую хотите внести")
                return
        await msg.answer("кредит не найден!")
    else:
        await msg.answer("Выберите кредит из списка ваших кредитов! /pay")
        await state.clear()


@router.message(PayForm.pay)
async def credit_pay3(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        amount = int(msg.text)
        if amount > 0:
            user = db.get_user(msg.from_user.id)
            if user.balance >= amount:
                cred = dc.get_credit((await state.get_data())["credit_id"])
                if dc.update_sum(cred.credit_id, cred.sum - amount) and db.add(
                    user.id, balance=-amount, lost_money=amount
                ):
                    await msg.answer("успешно!")
                    await state.clear()
                else:
                    await msg.answer("ашипка")
                    await state.clear()
            else:
                await msg.answer("У вас недостаточно для этого денег!")
                await state.clear()
        else:
            await msg.answer("Сумма должна быть целым числом /pay")
            await state.clear()
    else:
        await msg.answer("Сумма должна быть целым числом /pay")
        await state.clear()
