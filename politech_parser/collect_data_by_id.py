import asyncio
import json

import aiohttp
from aiohttp_retry import ExponentialRetry, RetryClient


DATA = {}

async def collect_data(session: aiohttp.ClientSession, id_: int):
    url = 'https://enroll.spbstu.ru/applications-manager/api/v1/admission-list/form'
    params = {
    'applicationEducationLevel': 'BACHELOR',
    'directionEducationFormId': '2',
    'directionId': str(id_),
    }
    retry_options = ExponentialRetry(attempts=5)
    retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session,
                               start_timeout=0.5)
    async with retry_client.get(url, params=params) as response:
        pass


# async def collect_all_data(session: aiohttp.ClientSession, directions: dict[str, str]):
#     tasks = []
#     for code, id_ in directions.items():
#         task = asyncio.create_task(collect_data(session, id_))
#         tasks.append(task)
#     asyncio.gather(*tasks)

#     # save DATA!