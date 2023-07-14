import asyncio
import json
from typing import Awaitable

import aiohttp
from aiohttp_retry import ExponentialRetry, RetryClient

JSON = {}

async def collect_directionsID(session: aiohttp.ClientSession, search: str) -> Awaitable:
    params = {
    'name': search,
    'educationFormId': '2',
    'educationLevelId': '2,5',
    'admissionBasis': 'BUDGET',
    'showClosed': 'true',
    }
    url = 'https://enroll.spbstu.ru/applications-manager/api/v1/directions/all-pageable'

    retry_options = ExponentialRetry(attempts=5)
    retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session,
                               start_timeout=0.5)
    async with retry_client.get(url, params=params) as response:
        if response.ok:
            resp = await response.json()
            for i in resp['result']:
                JSON[i['title']] = i['id']

async def parse_directions(session: aiohttp.ClientSession) -> Awaitable:
    tasks = []
    for i in map(lambda x: str(x).zfill(2), range(1, 67)):
        task = collect_directionsID(session, i)
        tasks.append(task)
    tasks.append(collect_directionsID(session, '38.05'))  # кодов с 38 больше чем 10...
    await asyncio.gather(*tasks)

    with open('directions.json', 'w', encoding='UTF-8') as file:
        json.dump(JSON, file, indent=4, ensure_ascii=False)



if __name__ == '__main__':

    async def main() -> Awaitable:
        async with aiohttp.ClientSession() as session:
            await parse_directions(session)

    asyncio.run(main())
