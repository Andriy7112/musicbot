from aiogram.types import Message

from admin.get_bot_stat import get_bot_stat_func
from keyboards.buttons import admin_buttons
from admin.send_everyone import send_everyone_func
from admin.backup_users_id import backup_users_id_func
from main import ADMIN_ID, bot, dp, ADMIN_LIST_COMMANDS


# Answer to admin commands
@dp.message_handler(lambda message: message.chat.id == int(ADMIN_ID) and message.text in ADMIN_LIST_COMMANDS)
async def admin_commands(message: Message):
    admin_command = message.text

    if message.text == 'Рассылка рекламы':
        await send_everyone_func()

    elif message.text == 'Бекап базы':
        await backup_users_id_func(message)

    elif message.text == 'Статистика бота':
        await get_bot_stat_func(message)

    elif admin_command == '/admin':
        await bot.send_message(ADMIN_ID, 'Все команды админа', reply_markup=admin_buttons)
