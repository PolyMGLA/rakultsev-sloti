from aiogram import types, BaseMiddleware
import aiogram

from typing import Callable, Dict, Awaitable, Any

from db import utils
import config

import traceback

import logging

logger = logging.getLogger(__name__)


class TGMiddleWare(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any],
    ):
        utils.update_visit(event)
        try:
            res = await handler(event, data)
            logger.debug(
                f"{event.from_user.username} ({event.from_user.id}): {event.text} | {event}"
            )
            return res
        except aiogram.exceptions.TelegramRetryAfter:
            logger.error("TelegramRetryAfter")
        except aiogram.exceptions.TelegramForbiddenError:
            logger.error("TelegramForbiddenError")
        except Exception as e:
            logger.error(str(e) + "\n" + traceback.format_exc())


class TGAdminMiddleWare(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any],
    ):
        if event.from_user.id in config.ADMINS:
            res = await handler(event, data)
            return res
        else:
            return await event.answer("ты недостоин")
