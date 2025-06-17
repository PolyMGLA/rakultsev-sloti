import asyncio
from datetime import datetime
from bot import bot

from db import dc

async def credits_task():
    while True:
        tekd = datetime.now().timestamp()
        credlist = dc.get_all_credits()
        for cred in credlist:
            if cred.last_date <= tekd:
                await bot.send_message(cred.user_id, "вы просрочили кредит! ваша мама умерла.")
            elif cred.next_date <= tekd:
                dc.update_next_date(cred.credit_id, cred.next_date + 86400)
                dc.update_sum(int(cred.sum * (1 + cred.perc / 100)))

        await asyncio.sleep(60)
