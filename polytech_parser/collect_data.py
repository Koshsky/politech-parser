import asyncio
import json
import os
from datetime import datetime
from typing import Any, Awaitable, Dict

import aiohttp
from aiohttp_retry import ExponentialRetry, RetryClient
from fake_useragent import UserAgent
from parse_directions import parse_directions


async def collect_data(session: aiohttp.ClientSession, title: str, id_: int) -> Awaitable:

    DATA: Dict[..., Any] = {}
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
        if response.ok:
            resp = await response.json()
            DATA['Бюджетных мест'] = resp['directionCapacity']
            DATA['Направление'] = title
            dt = datetime.strptime(resp['log']['datetime'], '%Y-%m-%dT%H:%M:%S')
            DATA['Время'] = dt.strftime('%A, %d. %B %Y %I:%M%p')

            DATA['Конкурс'] = {}
            for student in resp['list']:
                DATA['Конкурс'][student['userSnils']] = {
                    'Баллы': student['fullScore'],
                    'Без экзаменов': student['withoutExam'],
                    'Сдал оригинал': student['hasOriginalDocuments'],
                    'Приоритет': student['priority']
                }

    with open(f'parsed_data/{title.split()[0]}.json', 'w', encoding='UTF-8') as file:
        json.dump(DATA, file, ensure_ascii=False, indent=4)


async def collect_all_data(session: aiohttp.ClientSession, directions: Dict[str, Any]) -> Awaitable:
    tasks = []

    if not os.path.isdir('parsed_data'):
        os.mkdir('parsed_data')

    for title, id_ in directions.items():
        task = collect_data(session, title, id_)
        tasks.append(task)
    await asyncio.gather(*tasks)


async def update_lists() -> Awaitable:
    async with aiohttp.ClientSession(headers={'user-agent': UserAgent().random}) as session:
        if not os.path.isfile('directions.json'):
            await parse_directions(session)

        with open('directions.json', 'r', encoding='UTF-8') as file:
            directions = json.load(file)

        await collect_all_data(session, directions)


if __name__ == '__main__':
    asyncio.run(update_lists())
