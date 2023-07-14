import json
import re


def search_snils(snils: str):
    res = []
    with open('directions.json', 'r', encoding='UTF-8') as file:
        directions = json.load(file)['directions'].keys()
    for code in directions:
        with open(f'parsed_data/{code}.json', 'r', encoding='UTF-8') as f:
            data = json.load(f)
            for student in data['Конкурс']:
                if student['СНИЛС'] == snils:
                    res.append(data)
                    break
    return res


def snils_in_list(snils: str, json):
    for index, student in enumerate(json['Конкурс']):
        if student['СНИЛС'] == snils:
            break
    ball = json['Конкурс'][index]['Баллы']

    L = [i['СНИЛС'] for i in json['Конкурс']]
    L_orig = [i['СНИЛС'] for i in json['Конкурс'] if i['Сдал оригинал'] or i['СНИЛС'] == snils]

    res = f"{json['Направление']['title']}\n" \
          f"Бюджетных мест: {json['Бюджетных мест']}\n" \
          f"СНИЛС: {snils}\n" \
          f"Сумма баллов: {ball}\n" \
          f"Место в списке: {L.index(snils) + 1}/{json['Бюджетных мест']}\n" \
          f"Место в списке оригиналов: {L_orig.index(snils) + 1}/{json['Бюджетных мест']} " \
          f"(Оригинал {'еще не сдал' if not json['Конкурс'][index]['Сдал оригинал'] else 'сдал'})\n\n"
    return res


def verify_snils(snils: str):
    pattern = r'\b\d\d\d-\d\d\d-\d\d\d \d\d\b'
    return re.match(pattern, snils) is not None