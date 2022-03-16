import json
from uuid import uuid4

from utils.helpers import send_message
from main import EXPIRE_DATA_TIME, search_db

from utils.vk.vk_audio_api import VkApi
from utils.vk.vk_inline_call import get_audio_list_args


async def vk_audio_message_main(chat_id, user_text, lang):
    previous_search = search_db.get(user_text)
    if previous_search is None:
        json_id = str(uuid4())
        
        vk_api = VkApi()
        searched_audio = await vk_api.audio_search(user_text)

        if any(x == searched_audio for x in [None, {'count': 0, 'items': []}]):
            await send_message(chat_id, 'audio-search-unable', lang)
            return

        search_db.set(json_id, json.dumps(searched_audio), ex=EXPIRE_DATA_TIME)
        search_db.set(user_text, json_id, ex=EXPIRE_DATA_TIME)
    else:
        json_id = str(previous_search, 'utf-8')
        search_audio_response_db = search_db.get(json_id)
        searched_audio = json.loads(search_audio_response_db)

    args, inline_markup = await get_audio_list_args(json_id, searched_audio['items'], lang)
    await send_message(chat_id, 'audio-search-result', lang, markup=inline_markup, args=args)

