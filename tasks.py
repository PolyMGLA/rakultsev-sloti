import asyncio
from datetime import datetime
from bot import bot

from db import db, dc


async def credits_task():
    tekd = datetime.now().timestamp()
    credlist = dc.get_all_credits()
    for cred in credlist:
        if cred.sum <= 0:
            await bot.send_message(cred.user_id, "кредит успешно погашен!")
            dc.remove_credit(cred.credit_id)
        elif cred.last_date <= tekd:
            await bot.send_message(
                cred.user_id, "вы просрочили кредит! на ваш счет начислен штраф."
            )
            db.update_bal(
                cred.user_id,
                cred.user.balance
                - cred.sum * 5 * len(dc.get_user_credits(cred.user_id)),
            )
            dc.remove_credit(cred.credit_id)
        elif cred.next_date <= tekd:
            dc.update_next_date(cred.credit_id, cred.next_date + cred.cred_period)
            dc.update_sum(cred.credit_id, int(cred.sum * (1 + cred.perc / 100)))
