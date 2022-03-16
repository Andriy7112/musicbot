import asyncio

import aiohttp


async def get_music_seven(vk_audio_id):
    music_url = f'https://vk.music7s.cc/get.php?id={vk_audio_id}'

    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}
    async with aiohttp.ClientSession() as session:
        async with session.head(music_url, headers=headers) as get_music:
            music_headers = get_music.headers

            if 'Content-Length' in music_headers and int(music_headers['Content-Length']) > 1000:
                return music_url

            return None


if __name__ == '__main__':
    a = asyncio.run(get_music_seven('-2001196627_81196627'))
    print(a)
