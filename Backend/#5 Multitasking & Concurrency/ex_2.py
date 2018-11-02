import requests
import asyncio
import aiohttp
from time import time

SITES = [
    'www.google.com',
    'www.yandex.ru',
    'www.lenta.ru',
    'www.rbc.ru',
    'rg.ru',
    'vk.com',
    'habr.com',
    'rt.ru',
    'is74.ru']


def get_sync():
    t0 = time()
    for site in SITES:
        r = requests.get("https://" + site)
        print(r.url, r.status_code)
    t1 = time()
    print(f"Sync poll took {t1 - t0} seconds")


get_sync()


async def get_async(URL):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://" + URL) as resp:
            print(resp.real_url, resp.status)


async def async_main():
    t0 = time()
    tasks = [asyncio.ensure_future(get_async(site)) for site in SITES]
    await asyncio.gather(*tasks)
    t1 = time()
    print(f"Async poll took {t1 - t0} seconds")


loop = asyncio.get_event_loop()
loop.run_until_complete(async_main())
loop.close()
