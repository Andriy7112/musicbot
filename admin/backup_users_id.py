import csv
import os

from main import bot, users_db


async def backup_users_id_func(message):
    list_users_id = users_db.keys()

    file_name = '@Evomuzsavebot all users id with lang.csv'
    file_name_1 = '@Evomuzsavebot all users id.csv'
    file_name_2 = '@Evomuzsavebot all active users id.csv'

    with open(file_name, 'a', newline='') as csv_file:
        with open(file_name_1, 'a', newline='') as csv_file_1:
            with open(file_name_2, 'a', newline='') as csv_file_2:
                writer = csv.writer(csv_file)
                writer_1 = csv.writer(csv_file_1)
                writer_2 = csv.writer(csv_file_2)

                for user_id in list_users_id:
                    str_user_id = str(user_id, 'utf-8')
                    if not str_user_id.isdigit():
                        continue

                    user_lang_db = users_db.get(str_user_id)
                    user_lang = str(user_lang_db, 'utf-8')

                    writer.writerow([str_user_id, user_lang])
                    writer_1.writerow([str_user_id])

                    if user_lang != 'None':
                        writer_2.writerow([str_user_id])

    await bot.send_document(message.chat.id, open(file_name, 'rb'))
    await bot.send_document(message.chat.id, open(file_name_1, 'rb'))
    await bot.send_document(message.chat.id, open(file_name_2, 'rb'))

    os.remove(file_name)
    os.remove(file_name_1)
