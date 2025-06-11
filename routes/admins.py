from aiogram import Router, types, F
from aiogram.filters import Command, CommandObject

from db import db, dg, utils
from routes.keyboards import test_keyboard, admin_keyboard
from routes.utils import send_news
from bot import bot
from messages import ADMIN_HELP
from games import slots
from middlewares.telegram import TGMiddleWare, TGAdminMiddleWare

router = Router()
router.message.middleware(TGMiddleWare())
router.message.middleware(TGAdminMiddleWare())


@router.message(F.text.lower() == "📛админ-панель❌")
async def gay_panel(msg: types.Message):
    await msg.answer("Админ панель включена", reply_markup=admin_keyboard)


@router.message(F.text.lower() == "посмотреть секрет")
async def gay_secret_get(msg: types.Message):
    """
    [ADMIN ONLY] Просмотр секретной комбинации
    """
    await msg.answer("Секрет: " + slots.SECRET)


@router.message(F.text.lower() == "сгенерировать новый секрет")
async def gay_secret_regen(msg: types.Message):
    """
    [ADMIN ONLY] Генерация новой секретной комбинации
    """
    slots.secret_regen()
    await msg.answer("Новый секрет: " + slots.SECRET)


@router.message(Command("post"))
async def gay_novost(msg: types.Message, command: CommandObject):
    """
    [ADMIN ONLY] запостить новость всем пользователям
    """
    if command.args is None:
        await msg.answer("ашипка: напишите новость\n /post <новость>")
    else:
        await send_news(command.args)


@router.message(F.text.lower() == "количество участников")
async def gay_spisok(msg: types.Message):
    """
    [ADMIN ONLY] Вывод количества пользователей казика
    """
    users = db.users_list()
    if not users is None:
        await msg.answer(f"количество участников: {len(users)}")


@router.message(F.text.lower() == "список участников")
async def gay_spisok(msg: types.Message):
    """
    [ADMIN ONLY] Отправка списка всех участников.

    ВАЖНО! Отправляется каждый в отдельном сообщении, возможна ошибка отправки части из них вследствие большого кол-ва сообщений в минуту

    TODO: исправить
    """
    users = db.users_list()
    if not users is None:
        for u in users:
            await msg.answer(f"{u.name}, {u.id}")


@router.message(F.text.lower() == "тестирование")
async def gay_beta(msg: types.Message):
    await msg.answer("панель тестирования включена", reply_markup=test_keyboard)


@router.message(F.text.lower() == "помощь админам")
async def gay_admin_help(msg: types.Message):
    """
    [ADMIN ONLY] ПОМОЩЬ НЕМОЩНЫМ
    """
    await msg.answer(ADMIN_HELP)


@router.message(Command("balance"))
async def gay_balance(msg: types.Message, command: CommandObject):
    """
    [ADMIN ONLY] Просмотр баланса определенного человека
    """
    if command.args is None:
        await msg.answer("ашипка: напишите айди человека\n /balance <айди>")
    else:
        await msg.answer(f"{db.get_bal(command.args)}")


@router.message(Command("set_balance"))
async def gay_balance(msg: types.Message, command: CommandObject):
    """
    [ADMIN ONLY] Изменение баланса определенного человека
    """
    if command.args is None:
        await msg.answer("ашипка: не переданы аргументы")
        return
    try:
        id, ball = command.args.split(" ", maxsplit=1)
    except ValueError:
        await msg.answer(
            "ашипка: неправильный формат команды. Пример:\n"
            "/set_balance <id> <balance>"
        )
        return
    await msg.answer(f"{db.update_bal(id, ball)}")


@router.message(Command("user"))
async def gay_profile(msg: types.Message, command: CommandObject):
    """
    Инфо о профиле пользователя
    """
    if command.args == "":
        await msg.answer("Введите команду в формате /user <id>")
    else:
        msgid = int(command.args)
        await msg.answer(utils.profile(msgid))


@router.message(Command("gift"))
async def gay_get_gift(msg: types.Message, command: CommandObject):
    if not command.args:
        await msg.answer("Введите команду в формате /gift <gift_id>")
    else:
        gid = int(command.args)
        gift = dg.get_gift(gid)
        await msg.answer(f"{gift.gift_name} #{gift.gift_id} - \"{gift.descr}\"\nВладелец: {gift.user.name} ({gift.user_id})")


@router.message(Command("remove_gift"))
async def gay_remove_gift(msg: types.Message, command: CommandObject):
    if not command.args:
        await msg.answer("Введите команду в формате /remove_gift <gift_id>")
    else:
        gid = int(command.args)
        if dg.remove_gift(gid):
            await msg.answer("успешно")
        else:
            await msg.answer("ашипка")


@router.message(Command("gifts_list"))
async def gay_gifts_list(msg: types.Message):
    for gift in dg.get_all_gifts():
        await msg.answer(f"{gift.gift_name} #{gift.gift_id} - \"{gift.descr}\"\nВладелец: {gift.user.name} ({gift.user_id})")
