from db import db
from bot import bot

import logging

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
                    logging.info(f"sending to {u.id} failed: {e}")