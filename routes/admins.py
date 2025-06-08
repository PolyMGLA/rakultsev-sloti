from aiogram import Router, types, F, Bot
from aiogram.filters import Command, CommandObject

from db.database import db
import config
from bot import bot
from messages import ADMIN_HELP
from games import slots

router = Router()

async def send_news(text, exclude: list[int] = []):
    """
    Отправка новостей всем пользователям, за исключением списка exclude (аргумент опциональный)
    """
    users = db.users_list()
    if not users is None:
        for u in users:
            if u.id not in exclude:
                try:
                    await bot.send_message(u.id, "- НОВОСТЬ ОТ АДМИНА -\n" + text)
                except Exception as e:
                    print(f"sending to {u.id} failed: {e}")

@router.message(F.text.lower() == "посмотреть секрет")
async def gay_secret_get(msg: types.Message):
    """
    [ADMIN ONLY] Просмотр секретной комбинации
    """
    if msg.from_user.id in config.ADMINS:
        await msg.answer("Секрет: " + slots.SECRET)
    else:
        await msg.answer("ты недостоин")


@router.message(F.text.lower() == "сгенерировать новый секрет")
async def gay_secret_regen(msg: types.Message):
    """
    [ADMIN ONLY] Генерация новой секретной комбинации
    """
    if msg.from_user.id in config.ADMINS:
        slots.secret_regen()
        await msg.answer("Новый секрет: " + slots.SECRET)
    else:
        await msg.answer("ты недостоин")


@router.message(Command("novost"))
async def gay_novost(msg: types.Message, command: CommandObject):
    """
    [ADMIN ONLY] запостить новость всем пользователям
    """
    if msg.from_user.id in config.ADMINS:
        if command.args is None:
            await msg.answer("ашипка: напишите новость\n /novost <новость>")
            return
        await send_news(command.args)
    else:
        await msg.answer("ты недостоин")


@router.message(F.text.lower() == "количество участников")
async def gay_spisok(msg: types.Message):
    """
    [ADMIN ONLY] Вывод количества пользователей казика
    """
    schet = 0
    if msg.from_user.id in config.ADMINS:
            users = db.users_list()
            if not users is None:
                for u in users:
                    schet+=1
                await msg.answer(f"количество участников: {schet}")
    else:
        await msg.answer("ты недостоин")

@router.message(F.text.lower() == "список участников")
async def gay_spisok(msg: types.Message):
    """
    [ADMIN ONLY] Отправка списка всех участников.
    
    ВАЖНО! Отправляется каждый в отдельном сообщении, возможна ошибка отправки части из них вследствие большого кол-ва сообщений в минуту

    TODO: исправить
    """
    if msg.from_user.id in config.ADMINS:
            users = db.users_list()
            if not users is None:
                for u in users:
                    await msg.answer(f"{u.name}, {u.id}")
    else:
        await msg.answer("ты недостоин")

@router.message(F.text.lower() == "помощь админам")
async def gay_admin_help(msg:types.Message):
    """
    [ADMIN ONLY] ПОМОЩЬ НЕМОЩНЫМ
    """
    if msg.from_user.id in config.ADMINS:
        await msg.answer(ADMIN_HELP)
    else:
        await msg.answer("ты недостоин")

@router.message(Command("balance"))
async def gay_balance(msg: types.Message, command: CommandObject):
    """
    [ADMIN ONLY] Просмотр баланса определенного человека
    """
    if msg.from_user.id in config.ADMINS:
        if command.args is None:
            await msg.answer("ашипка: напишите айди человека\n /balance <айди>")
            return
        await msg.answer(f"{db.get_bal(command.args)}")
    else:
        await msg.answer("ты недостоин")

@router.message(Command("set_balance"))
async def gay_balance(msg: types.Message, command: CommandObject):
    """
    [ADMIN ONLY] Изменение баланса определенного человека
    """
    if msg.from_user.id in config.ADMINS:
        if command.args is None:
            await msg.answer(
                "ашипка: не переданы аргументы"
            )
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
    else:
        await msg.answer("ты недостоин")