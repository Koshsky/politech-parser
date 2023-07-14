import asyncio
import json
from pprint import pprint

import aiohttp
from aiohttp_retry import ExponentialRetry, RetryClient


SNILSES = []
with open('directions.json', 'r', encoding='UTF-8') as file:
    directions = json.load(file)['directions']

async def collect_data(session: aiohttp.ClientSession, code: str, id_: int):
    global SNILSES
    global directions
    DATA = {}
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
        resp = await response.json()
        try:
            DATA['Бюджетных мест'] = resp['directionCapacity']
        except KeyError:
            pprint(resp)
        DATA['Направление'] = directions[code]
        students = []
        for student in resp['list']:
            students.append({
                'Баллы': student['fullScore'],
                'Без экзаменов': student['withoutExam'],
                'СНИЛС': student['userSnils'],
                'Сдал оригинал': student['hasOriginalDocuments']

            })
            SNILSES.append(student['userSnils'])
        students.sort(key=lambda x: (x['Без экзаменов']==False, -x['Баллы']))
        DATA['Конкурс'] = students
    with open(f'parsed_data/{code}.json', 'w', encoding='UTF-8') as file:
        json.dump(DATA, file, ensure_ascii=False, indent=4)


async def collect_all_data(session: aiohttp.ClientSession):
    tasks = []
    global directions
    for code, staff in directions.items():
        id_ = staff['id']
        task = asyncio.create_task(collect_data(session, code, id_))
        tasks.append(task)
    await asyncio.gather(*tasks)
    with open(f'parsed_data/SNILSES.txt', 'w', encoding='UTF-8') as file:
        file.write('\n'.join(SNILSES))

if __name__ == '__main__':
    import config

    async def main():
        async with aiohttp.ClientSession(headers=config.headers, cookies=config.cookies) as session:

            await collect_all_data(session)
    asyncio.run(main())