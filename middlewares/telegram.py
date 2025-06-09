from aiogram import types, BaseMiddleware

from typing import Callable, Dict, Awaitable, Any

import logging
logging.basicConfig(level=logging.DEBUG, filename="logs.log",filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)

class TGMiddleWare(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.Message,
            data: Dict[str, Any]
    ):
        res = await handler(event, data)
        logger.debug(event)
        return res