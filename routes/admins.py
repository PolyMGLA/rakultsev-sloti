from aiogram import Router, types, F
from aiogram.filters import Command, CommandObject, or_f

from datetime import datetime

from db import db, dg, dc, utils
from routes.keyboards import test_keyboard, admin_keyboard
from routes.utils import send_news
from messages import ADMIN_HELP
from games import slots
from bot import bot, dp, scheduler
from middlewares.telegram import TGAdminMiddleWare
from market.data import data

router = Router()
router.message.middleware(TGAdminMiddleWare())


@router.message(F.text.lower() == "📛админ-панель❌")
async def gay_panel(msg: types.Message):
    await msg.answer("Админ панель включена", reply_markup=admin_keyboard)


@router.message(F.text == "📦биржа💰")
async def gay_marketplace(msg: types.Message):
    await msg.answer(
        f"Информация о бирже Rakom:" + f"\nКурс HamsterCoin: {data.hamster_course}"
    )


@router.message(or_f(F.text.lower() == "посмотреть секрет", Command("secret")))
async def gay_secret_get(msg: types.Message):
    """
    [ADMIN ONLY] Просмотр секретной комбинации
    """
    await msg.answer("Секрет: " + slots.SECRET)


@router.message(
    or_f(F.text.lower() == "сгенерировать новый секрет", Command("secret_gen"))
)
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


@router.message(or_f(F.text.lower() == "количество участников", Command("user_num")))
async def gay_spisok(msg: types.Message):
    """
    [ADMIN ONLY] Вывод количества пользователей казика
    """
    users = db.users_list()
    if not users is None:
        await msg.answer(f"количество участников: {len(users)}")


@router.message(or_f(F.text.lower() == "список участников", Command("user_list")))
async def gay_spisok(msg: types.Message):
    """
    [ADMIN ONLY] Отправка списка всех участников.

    ВАЖНО! Отправляется каждый в отдельном сообщении, возможна ошибка отправки части из них вследствие большого кол-ва сообщений в минуту

    TODO: исправить
    """
    users = db.users_list()
    if not users is None:
        for u in users:
            await msg.answer(f"{u.prefix}{u.name}, {u.id}")


@router.message(or_f(F.text.lower() == "тестирование", Command("test")))
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
        await msg.answer(f"{db.get(command.args, 'balance')}")


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
    await msg.answer(f"{db.update(id, balance=ball)}")


@router.message(Command("user"))
async def gay_profile(msg: types.Message, command: CommandObject):
    """
    Инфо о профиле пользователя
    """
    if command.args == "":
        await msg.answer("Введите команду в формате /user <id>")
    else:
        msgid = int(command.args)
        await msg.answer(utils.profile(msgid, show_id=True))


@router.message(Command("gift"))
async def gay_get_gift(msg: types.Message, command: CommandObject):
    if not command.args:
        await msg.answer("Введите команду в формате /gift <gift_id>")
    else:
        gid = int(command.args)
        gift = dg.get_gift(gid)
        await msg.answer(
            f'{gift.gift_name} #{gift.gift_id} - "{gift.descr}"\nВладелец: {gift.user.prefix}{gift.user.name} ({gift.user_id})'
        )


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
        await msg.answer(
            f'{gift.gift_name} #{gift.gift_id} - "{gift.descr}"\nВладелец: {gift.user.prefix}{gift.user.name} ({gift.user_id})'
        )


@router.message(Command("find_users"))
async def gay_find_users(msg: types.Message, command: CommandObject):
    if command.args is None:
        await msg.answer("Введите команду в формате /find_users <username>")
    else:
        users = db.users_list()
        users = list(filter(lambda x: x.name.startswith(command.args), users))
        if users:
            await msg.answer("\n".join(f"{u.name} - {u.id}" for u in users))
        else:
            await msg.answer("не найдено")


@router.message(Command("credit"))
async def gay_credit(msg: types.Message, command: CommandObject):
    await msg.answer(utils.credit(int(command.args), show_user=True))


@router.message(Command("credit_list"))
async def gay_credit_list(msg: types.Message):
    for cred in dc.get_all_credits():
        await msg.answer(utils.credit(cred.credit_id, show_user=True))


@router.message(Command("get_minus"))
async def gay_minus(msg: types.Message):
    users = list(filter(lambda x: x.balance < 0, sorted(db.users_list(), key=lambda x: -x.balance)))
    await msg.answer(
        "\n".join(f"{user.name} ({user.id}) - {user.balance}" for user in users) 
    )


@router.message(Command("exec"))
async def gay_exec(msg: types.Message, command: CommandObject):
    whitelist_globals = {"__builtins__": {"int": int}, "db": db, "dg": dg, "dc": dc, "datetime": datetime}
    if command.args is None:
        await msg.answer('Введите команду в формате "/exec 1"')
    else:
        try:
            await msg.answer(str(eval(command.args, whitelist_globals)))
        except Exception as e:
            await msg.answer(str(e))


@router.message(Command("send_db"))
async def gay_send_db(msg: types.Message):
    doc = types.FSInputFile("./db.db")
    await msg.answer_document(doc, caption="База данных")


@router.message(Command("exit"))
async def gay_exit(msg: types.Message, command: CommandObject):
    if command.args is None or command.args.strip() != "yes":
        await msg.answer('Напишите "/exit yes", если точно хотите выключить бота')
    else:
        await msg.answer("Выключение бота..")
        await dp.stop_polling()
        scheduler.shutdown(wait=False)
