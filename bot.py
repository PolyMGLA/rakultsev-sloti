from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config

bot = Bot(config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher()

scheduler = AsyncIOScheduler()