import json
import os
from datetime import datetime


def open_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        """Чтение из JSON файла"""
        list_transaction = json.load(file)
        list_transaction = [j for j in list_transaction if j]
        return list_transaction


def sort_data_list_transaction(list_transaction):
    """Сортировка списка транзакций по дате"""
    sort_data_lst_trans = sorted(list_transaction,
                                 key=lambda x: datetime.strptime(x["date"], '%Y-%m-%dT%H:%M:%S.%f'),
                                 reverse=True)
    return sort_data_lst_trans


def sort_state_list_transaction(sort_data_lst_trans):
    """Сортировка списка транзакций по ключу state"""
    sort_state_lst_trans = sorted(sort_data_lst_trans, key=lambda x: x["state"], reverse=True)
    return sort_state_lst_trans


def data_func(data_time):
    """Преобразование даты к формату %d.%m.%Y"""
    data_transformation = datetime.strptime(data_time, '%Y-%m-%dT%H:%M:%S.%f')
    data = data_transformation.strftime('%d.%m.%Y')
    return data


def cards_transformation(info):
    """Номер карты замаскирован и не отображается целиком в формате  XXXX XX** **** XXXX"""
    card_num = info.split()
    card_name = card_num[0] if len(card_num) < 3 else card_num[0] + ' ' + card_num[1]
    hidden_card = card_num[-1][:4] + ' ' + card_num[-1][4:6] + '** **** ' + card_num[-1][-4:]
    return f'{card_name} {hidden_card}'


def account_transformation(info):
    """Номер счета замаскирован и не отображается целиком в формате  **XXXX (полдение 4 цифры)"""
    account_num = info.split()
    return f'{account_num[0]} **{account_num[1][-4:]}'


def displaying_last_five_transactions():
    file = open_file(os.path.join('../', 'date', 'operations.json'))
    transaction_sort_data = sort_data_list_transaction(file)
    transaction = sort_state_list_transaction(transaction_sort_data)

    for i in range(5):
        if transaction[i]['description'] == 'Открытие вклада':
            print(f'{data_func(transaction[i]['date'])} {transaction[i]['description']}\n'
                  f'{account_transformation(transaction[i]['to'])}\n{transaction[i]['operationAmount']['amount']} '
                  f'{transaction[i]['operationAmount']['currency']['name']}\n')
        elif transaction[i]['description'] == 'Перевод со счета на счет':
            print(f'{data_func(transaction[i]['date'])} {transaction[i]['description']}\n'
                  f'{account_transformation(transaction[i]['from'])} -> '
                  f'{account_transformation(transaction[i]['to'])}\n'
                  f'{transaction[i]['operationAmount']['amount']} '
                  f'{transaction[i]['operationAmount']['currency']['name']}\n')
        elif transaction[i]['description'] == 'Перевод с карты на карту':
            print(f'{data_func(transaction[i]['date'])} {transaction[i]['description']}\n'
                  f'{cards_transformation(transaction[i]['from'])} -> {cards_transformation(transaction[i]['to'])}\n'
                  f'{transaction[i]['operationAmount']['amount']} '
                  f'{transaction[i]['operationAmount']['currency']['name']}\n')
        else:
            if transaction[i]['from'][0] == 'Счет':
                print(f'{data_func(transaction[i]['date'])} {transaction[i]['description']}\n'
                      f'{account_transformation(transaction[i]['from'])} -> '
                      f'{account_transformation(transaction[i]['to'])}\n'
                      f'{transaction[i]['operationAmount']['amount']} '
                      f'{transaction[i]['operationAmount']['currency']['name']}\n')
            else:
                print(f'{data_func(transaction[i]['date'])} {transaction[i]['description']}\n'
                      f'{cards_transformation(transaction[i]['from'])} -> '
                      f'{account_transformation(transaction[i]['to'])}\n'
                      f'{transaction[i]['operationAmount']['amount']} '
                      f'{transaction[i]['operationAmount']['currency']['name']}\n')
    return ''
