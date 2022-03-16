from main import bot, files_id, users_db


async def get_bot_stat_func(message):
    sent_message = await bot.send_message(message.chat.id, 'Пожалуйста, подождите')

    statistics = files_id.get('STATISTICS')
    if statistics is None:
        files_id.set('STATISTICS', 0)
        statistics = 0

    users_count = users_db.dbsize()

    admin_text = '*Статистика бота*:\n' \
                 'Пользователей всего: *{0:,}*\n' \
                 'Скачиваний всего: *{1:,}*'.format(users_count, int(statistics))

    await bot.send_message(message.chat.id, admin_text, parse_mode='markdown')
    await bot.delete_message(message.chat.id, sent_message.message_id)
