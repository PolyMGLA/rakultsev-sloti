from aiogram import types, F, Router

router = Router()

user_data = {}


def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="-10", callback_data="num_decr10"),
            types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
            types.InlineKeyboardButton(text="+1", callback_data="num_incr"),
            types.InlineKeyboardButton(text="+10", callback_data="num_incr10"),
        ],
        [types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def update_num_text(message: types.Message, new_value: int):
    await message.edit_text(f"Укажите ставку: {new_value}", reply_markup=get_keyboard())


@router.message(F.text.lower() == "✨сосать✨")
async def gay_stavka(message: types.Message):
    user_data[message.from_user.id] = 2
    await message.answer("Укажите ставку: 2", reply_markup=get_keyboard())


@router.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split("_")[1]
    if user_value >= 12:
        if action == "incr":
            user_data[callback.from_user.id] = user_value + 1
            await update_num_text(callback.message, user_value + 1)
        elif action == "incr10":
            user_data[callback.from_user.id] = user_value + 10
            await update_num_text(callback.message, user_value + 10)
        elif action == "decr":
            user_data[callback.from_user.id] = user_value - 1
            await update_num_text(callback.message, user_value - 1)
        elif action == "decr10":
            user_data[callback.from_user.id] = user_value - 10
            await update_num_text(callback.message, user_value - 10)

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
