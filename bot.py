from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from redis.asyncio import Redis

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config

redis = Redis(host="127.0.0.1", port=6379, db=0)
bot = Bot(config.BOT_TOKEN)
storage = None # Желательно: RedisStorage(redis)
if not storage:
    storage = MemoryStorage()
dp = Dispatcher(storage=storage)

scheduler = AsyncIOScheduler()
