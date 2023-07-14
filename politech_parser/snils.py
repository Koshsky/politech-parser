import json


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
    for student in json['Конкурс']:
        if student['СНИЛС'] == snils:
            ball = student['Баллы']
            break

    L = [i['СНИЛС'] for i in json['Конкурс']]
    L_orig = [i['СНИЛС'] for i in json['Конкурс'] if i['Сдал оригинал']]

    res = f"{json['Направление']['title']}\n" \
          f"Бюджетных мест: {json['Бюджетных мест']}\n" \
          f"СНИЛС: {snils}\n" \
          f"Сумма баллов: {ball}\n" \
          f"Место в списке: {L.index(snils) + 1}/{json['Бюджетных мест']}\n"
    if snils in L_orig:
        res += f"Место в списке оригиналов: {L_orig.index(snils) + 1}/{json['Бюджетных мест']}\n"

    return res+'\n'