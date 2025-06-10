from aiogram import types

menu_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="🎰Cлоты🎰"),
            types.KeyboardButton(text="♣Блекджек🃏"),
        ],
        [
            # types.KeyboardButton(text="🔥Правила🔥"),
            types.KeyboardButton(text="👥Посетители👥"),
            types.KeyboardButton(text="👾Профиль👾"),
        ],
        [
            types.KeyboardButton(text="🆘Помощь🆘"),
            types.KeyboardButton(text="🔝Топ казино🎰"),
        ],
        [
            types.KeyboardButton(text="📛Админ-панель❌"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите что хотите сделать",
)

slots_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="✨крутить✨"),
            types.KeyboardButton(text="💲мега ласт деп💲"),
        ],
        [
            types.KeyboardButton(text="🔥Правила слотов🔥"),
            types.KeyboardButton(text="👾Профиль👾"),
        ],
        [
            types.KeyboardButton(text="🆘Помощь🆘"),
            types.KeyboardButton(text="🔝Топ казино🎰"),
        ],
        [
            types.KeyboardButton(text="🔙Назад🔙"),
        ],
        [
            types.KeyboardButton(text="📛Админ-панель❌"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите что хотите сделать",
)

blackjack_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="✨играть✨"),
            types.KeyboardButton(text="💲мега ласт деп💲"),
        ],
        [
            types.KeyboardButton(text="🔥Правила блэкджека🔥"),
            types.KeyboardButton(text="👾Профиль👾"),
        ],
        [
            types.KeyboardButton(text="🆘Помощь🆘"),
            types.KeyboardButton(text="🔝Топ казино🎰"),
        ],
        [
            types.KeyboardButton(text="🔙Назад🔙"),
        ],
        [
            types.KeyboardButton(text="📛Админ-панель❌"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите что хотите сделать",
)

admin_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="количество участников"),
            types.KeyboardButton(text="список участников"),
        ],
        [
            types.KeyboardButton(text="посмотреть секрет"),
            types.KeyboardButton(text="сгенерировать новый секрет"),
        ],
        [types.KeyboardButton(text="тестирование")],
        [types.KeyboardButton(text="помощь админам")],
        [types.KeyboardButton(text="🔙назад🔙")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите что хотите сделать",
)

test_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="✨сосать✨")],
        [types.KeyboardButton(text="📛Админ-панель❌")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите что хотите сделать",
)
