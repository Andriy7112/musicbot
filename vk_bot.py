from aiogram.utils import executor

import handlers
from utils.help_functions import on_startup
from main import dp


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
