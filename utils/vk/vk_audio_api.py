import json
import random
import asyncio

import aiohttp
import requests

AUDIO_TOKENS = [
    '34ac4302f1d2da0806db4f74733c5e48dd1119ea50d13df459caf72c75526c47ab10223df742f84f99551',
    '25ef0a6bc44d735d686e2970f0810bb201c052448cc6a5deaa71c4e4a2ee4d8e19bc67c7f612923d382c5',
    '92f9cae8b3b6ac1f64f5eb244289ee7f1dc425796731405b3419f5e1a04317bdb3308949b5101b12591cc',
    'faaf9fb895ad7c9186b25ce0ae9e9ec95a44e12615ad7b6134b213cf3d0a34f29dc99e590ad868f048ef4',
    '4c6d4709398c1641528c11b826650f049e358c9a470d7b46525264d97c775234fe091030de36e7ddc077f',
    '46f16faaa9e8b076661KXN5C6h7vNncMwSnLoxTxPdVnpQsCdedR3765d0e742bfddad3965d0e7853815734',
    '7850a8a643217121e85450cf8d802630976564ff852d7357604e36b901652a0c921c1c95eb1eeb1663d7d',
]
print(AUDIO_TOKENS)


URL = "https://api.vk.com/method/{}"

VK_AUDIO_VERSION = '5.95'
HEADERS_AUDIO = {'User-Agent': 'KateMobileAndroid/56 lite-460 (Android 4.4.2; SDK 19; '
                               'x86; unknown Android SDK built for x86; en)'}

# HEADERS_AUDIO = {'User-Agent': 'VKAndroidApp/5.52-4543 (Android 5.1.1; SDK 22; x86_64; unknown Android SDK built for x86_64; en; 320x240)'}

CATALOG_AUDIO_VERSION = '5.103'
CATALOG_HEADERS = {"User-Agent": "VKAndroidApp/5.52-4543 (Android 5.1.1; SDK 22; x86_64; "
                                 "unknown Android SDK built for x86_64; en; 320x240)"}


async def run_api():
    for token in AUDIO_TOKENS:
        vk_api = VkApi(token)
        response = await vk_api.audio_search('miyagi')
        if response is None:
            print(token, 'error')
        else:
            print(token, 'success')


class VkApi:
    # Create session
    def __init__(self, token=None):
        self.token = token
        self.session = aiohttp.ClientSession()

    # Function for all functions to make request
    async def __make_request(self, method, params):
        if self.token is None:
            params['access_token'] = random.choice(AUDIO_TOKENS)
        else:
            params['access_token'] = self.token

        params['v'] = VK_AUDIO_VERSION
        headers = HEADERS_AUDIO

        get_request = await self.session.get(URL.format(method), params=params, headers=headers)
        request_text = await get_request.content.read()
        request_json = json.loads(request_text)

        if 'response' in request_json:
            response_json = request_json['response']
        else:
            response_json = None

        await self.session.close()
        return response_json

    async def audio_search(self, audio_name, count=100):
        params = {'q': audio_name, 'count': count}
        response_json = await self.__make_request('audio.search', params)
        return response_json


if __name__ == '__main__':
    asyncio.run(run_api())
