import json
import re
from typing import Any, Dict, List


def verify_snils(snils: str) -> bool:
    pattern = r'\b\d\d\d-\d\d\d-\d\d\d \d\d\b'
    return re.match(pattern, snils) is not None


def sort_snilses_by_ball(students: Dict[str, Any]) -> List[str]:
    sort_f = lambda x: (students[x]['Без экзаменов']==False, -students[x]['Баллы'])
    snilses = list(sorted(students.keys(), key=sort_f))
    return snilses


def search_snils(SNILS: str) -> List[Dict[str, Any]]:
    res = []
    with open('directions.json', 'r', encoding='UTF-8') as file:
        titles = json.load(file).keys()
    for code in map(lambda x: x.split()[0], titles):
        with open(f'parsed_data/{code}.json', 'r', encoding='UTF-8') as f:
            data = json.load(f)
            if SNILS in data['Конкурс']:
                res.append(data)
    return res


def format_snils_result(snils: str, json: Dict[str, Any]) -> str:
    ball = json['Конкурс'][snils]['Баллы']

    sorted_snilses = sort_snilses_by_ball(json['Конкурс'])
    L = [i for i in sorted_snilses]
    L_orig = [i for i in sorted_snilses if json['Конкурс'][i]['Сдал оригинал'] or i == snils]

    res = f"{json['Направление']}\n" \
          f"Бюджетных мест: {json['Бюджетных мест']}\n" \
          f"Приоритет: {json['Конкурс'][snils]['Приоритет']}\n" \
          f"Сумма баллов: {ball}\n" \
          f"Место в списке: {L.index(snils) + 1}/{json['Бюджетных мест']}\n" \
          f"Место в списке оригиналов: {L_orig.index(snils) + 1}/{json['Бюджетных мест']} " \
          f"(Оригинал {'еще не ' if not json['Конкурс'][snils]['Сдал оригинал'] else ''}сдал)\n\n"

    return res
