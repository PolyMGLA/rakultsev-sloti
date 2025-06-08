                                                                    #импорт всякой залупы
import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

from db.database import db, dt
import routes.slots
import routes.admins
from routes.keyboards import *
import config
from messages import HELP, RULES

from datetime import datetime


bot = Bot(config.BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def gay_start(msg: types.Message):
    """
    Регистрация пользователя (попытка зарегать)
    """
    if db.register(
        msg.from_user.id,
        ("@" + msg.from_user.username) if not msg.from_user.username is None else msg.from_user.full_name
        ) and dt.add_user(msg.from_user.id):
        await msg.answer("Регистрация успешна!\n/menu - главное меню")
    else:
        await msg.answer("Регистрация не удалась, поплачь(\n/menu - главное меню")


@dp.message(F.text.lower() == "🆘помощь🆘")
async def gay_help(msg: types.Message):
    """
    Собсна текст помощи утопающим
    """
    await msg.answer(HELP)


@dp.message(F.text.lower() == "👾профиль👾")
async def gay_profile(msg: types.Message):
    """
    Инфо о профиле пользователя
    """
    user = db.get_user(msg.from_user.id)
    if user is None or user == False:
        await msg.answer("Вы не зарегистрированы!\n/start")
    await msg.answer(
        f"Пользователь: {user.name}"
         + f"\nБаланс: {user.balance}" + (" (вы в долгах)" if user.balance < 0 else "")
         + f"\nКруток слотов: {user.slots_num}"
         + f"\nДодепов: {user.dodep_num}"
        )


@dp.message(F.text.lower() == "🔥правила🔥")
async def gay_ref(msg: types.Message):
    """
    Текст правил всех игр (мне точно надо это писать?)
    """
    await msg.answer(RULES)


@dp.message(F.text.lower() == "💲мега ласт деп💲")
async def gay_dodep(msg: types.Message):
    """
    Функция для пополнения баланса на аккаунте (собственно говоря, додеп)
    """
    user = db.get_user(msg.from_user.id)
    if user.balance < 2:
        if dt.get_date(msg.from_user.id) is None:
            dt.add_user(msg.from_user.id)

        tdt = int(datetime.now().timestamp())
        last_dodep = dt.get_date(msg.from_user.id).date
        if tdt - last_dodep < 600:
            await msg.answer(f"подождите {(600 - tdt + last_dodep) // 60} минут {(600 - tdt + last_dodep) % 60} секунд")
        else:
            if db.update_bal(msg.from_user.id, 100) and db.add_dodep(msg.from_user.id) and dt.set_date(msg.from_user.id, tdt):
                await msg.answer("додеп прошел")
            else:
                await msg.answer("додеп не прошел")
    else:
        await msg.answer("вы слишком богатые")


@dp.message(F.text.lower() == "🔝топ казино🎰")
async def gay_top(msg: types.Message):
    """
    Топ казино по балансу, круткам слотов и додепам
    """
    top = db.top5_money()
    res = ""

    res += "Топ по счету:\n"
    if top == False:
        res += "ашипка\n\n"
    else:
        res += "\n".join([f"{i + 1}. {top[i].name} - {top[i].balance}" for i in range(len(top))]) + "\n\n"

    top = db.top5_slots()
    res += "Топ по круткам:\n"
    if top == False:
        res += "ашипка\n\n"
    else:
        res += "\n".join([f"{i + 1}. {top[i].name} - {top[i].slots_num}" for i in range(len(top))]) + "\n\n"
    
    top = db.top5_dodeps()
    res += "Топ по додепам:\n"
    if top == False:
        res += "ашипка\n\n"
    else:
        res += "\n".join([f"{i + 1}. {top[i].name} - {top[i].dodep_num}" for i in range(len(top))]) + "\n\n"

    await msg.answer(res)


@dp.message(Command("menu"))
async def gay_menu(msg: types.Message):
    await msg.answer("Добро пожаловать, великий додепер", reply_markup=menu_keyboard)


@dp.message(F.text.lower() == "♣блекджек🃏")
async def gay_menu_blackjack(msg: types.Message):
    await msg.answer("Добро пожаловать в блекджек", reply_markup=menu_keyboard)


@dp.message(F.text.lower() == "🎰cлоты🎰")
async def gay_menu_slots(msg: types.Message):
    await msg.answer("Добро пожаловать в слоты", reply_markup=slots_keyboard)


@dp.message(F.text.lower() == "🔙назад🔙")
async def gay_back(msg: types.Message):
    await msg.answer("Добро пожаловать в меню", reply_markup=menu_keyboard)


@dp.message(F.text.lower() == "📛админ-панель❌")
async def gay_panel(msg: types.Message):
    if msg.from_user.id in config.ADMINS:
        await msg.answer("Админ панель включена", reply_markup=admin_keyboard)
    else:
        await msg.answer("ты недостоин")

user_data = {}

def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="-10", callback_data="num_decr10"),
            types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
            types.InlineKeyboardButton(text="+1", callback_data="num_incr"),
            types.InlineKeyboardButton(text="+10", callback_data="num_incr10"),
        ],
        [types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def update_num_text(message: types.Message, new_value: int):
    await message.edit_text(
        f"Укажите ставку: {new_value}",
        reply_markup=get_keyboard()
    )


@dp.message(F.text.lower() == "✨играть✨")
async def gay_stavka(message: types.Message):
    user_data[message.from_user.id] = 2
    await message.answer("Укажите ставку: 2", reply_markup=get_keyboard())


@dp.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split("_")[1]
    if user_value >= 12:
        if action == "incr":
            user_data[callback.from_user.id] = user_value+1
            await update_num_text(callback.message, user_value+1)
        elif action == "incr10":
            user_data[callback.from_user.id] = user_value+10
            await update_num_text(callback.message, user_value+10)
        elif action == "decr":
            user_data[callback.from_user.id] = user_value-1
            await update_num_text(callback.message, user_value-1)
        elif action == "decr10":
            user_data[callback.from_user.id] = user_value-10
            await update_num_text(callback.message, user_value-10)

        elif action == "finish":
            await callback.message.edit_text(f"Ваша ставка: {user_value}")

        await callback.answer()
    elif user_value > 2:
        if action == "incr":
            user_data[callback.from_user.id] = user_value + 1
            await update_num_text(callback.message, user_value + 1)
        elif action == "incr10":
            user_data[callback.from_user.id] = user_value + 10
            await update_num_text(callback.message, user_value + 10)
        elif action == "decr":
            user_data[callback.from_user.id] = user_value - 1
            await update_num_text(callback.message, user_value - 1)
        elif action == "finish":
            await callback.message.edit_text(f"Ваша ставка: {user_value}")
        await callback.answer()
    else:
        if action == "incr":
            user_data[callback.from_user.id] = user_value + 1
            await update_num_text(callback.message, user_value + 1)
        elif action == "incr10":
            user_data[callback.from_user.id] = user_value + 10
            await update_num_text(callback.message, user_value + 10)
        elif action == "finish":
            await callback.message.edit_text(f"Ваша ставка: {user_value}")
        await callback.answer()


async def main():
    print("starting bot..")

    dp.include_router(routes.slots.router)
    dp.include_router(routes.admins.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())