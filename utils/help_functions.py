from uuid import uuid4

import aiofiles
import aiohttp

from utils.helpers import send_message, get_chat_member
from main import files_id, ADMIN_ID, CHANNEL_ID


async def save_user_actions():
    statistics = files_id.get('STATISTICS')
    if statistics is None:
        files_id.set('STATISTICS', 0)
        statistics = 0

    total_stat = int(statistics) + 1
    files_id.set('STATISTICS', total_stat)


# Send notification that bot started working
async def on_startup(args):  # send errors to admin
    await send_message(ADMIN_ID, 'admin-bot-started', 'ru')


async def download_vk_music(download_url):
    directory = 'music/{}.mp3'.format(str(uuid4()))

    async with aiohttp.ClientSession() as session:
        async with session.get(download_url) as get_request:
            file = await aiofiles.open(directory, mode='wb')
            get_request_content = await get_request.read()
            await file.write(get_request_content)
            await file.close()

    return directory


async def check_channel_following(chat_id):
    try:
        user_channel_news = await get_chat_member(CHANNEL_ID, chat_id)
        if user_channel_news['status'] == 'creator' or user_channel_news['status'] == 'administrator':
            return True

        if user_channel_news['status'] != 'member':
            return False
        return True
    except:
        return False
