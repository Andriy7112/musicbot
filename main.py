import asyncio
import redis
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from data.config import BOT_TOKEN

loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=loop)

files_id = redis.StrictRedis(host='localhost', port=6379, db=1)
users_db = redis.StrictRedis(host='localhost', port=6379, db=2)
search_db = redis.StrictRedis(host='localhost', port=6379, db=3)

EXPIRE_DATA_TIME = 3600 * 24  # 24 Hours
EXPIRE_START_RESULTS = 3600 * 12  # 12 Hours

# ADMIN_ID = 653391824
ADMIN_ID = 294915223
AD_CHANNEL_ID = -1001364313621
CHANNEL_ID = -1001141156919

ADMIN_LIST_COMMANDS = ['Рассылка рекламы', '/admin', 'Бекап базы', 'Статистика бота']


class AdminSendEveryOne(StatesGroup):
    ask_lang = State()
    ask_post = State()
    ask_send = State()
