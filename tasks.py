import asyncio
from datetime import datetime
from bot import bot

from db import db, dc

import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="logs.log",
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)

async def credits_task():
    tekd = datetime.now().timestamp()
    credlist = dc.get_all_credits()
    for cred in credlist:
        try:
            if cred.sum <= 0:
                await bot.send_message(cred.user_id, "кредит успешно погашен!")
                dc.remove_credit(cred.credit_id)
            elif cred.last_date <= tekd:
                sm = cred.sum * 5 * len(dc.get_user_credits(cred.user_id))
                db.add(
                    cred.user_id,
                    balance=-sm,
                    lost_money=sm
                )
                dc.remove_credit(cred.credit_id)
                await bot.send_message(
                    cred.user_id, "вы просрочили кредит! на ваш счет начислен штраф."
                )
            elif cred.next_date <= tekd:
                dc.update_next_date(cred.credit_id, cred.next_date + cred.cred_period)
                dc.update_sum(cred.credit_id, int(cred.sum * (1 + cred.perc / 100)))
        except Exception as e:
            logger.error(str(e))
