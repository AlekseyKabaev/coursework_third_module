from src.utils import data_func, cards_transformation, account_transformation, sort_data_list_transaction


def test_sort_data_list_transaction1():
    assert data_func("2019-08-26T10:50:58.294041") == "26.08.2019"


def test_sort_data_list_transaction2():
    assert data_func("2019-07-03T18:35:29.512364") == "03.07.2019"


def test_cards_transformation1():
    assert cards_transformation('MasterCard 7158300734726758') == 'MasterCard 7158 30** **** 6758'


def test_cards_transformation2():
    assert cards_transformation('Visa Classic 6831982476737658') == 'Visa Classic 6831 98** **** 7658'


def test_account_transformation1():
    assert account_transformation('Счет 48894435694657014368') == 'Счет **4368'


def test_account_transformation2():
    assert account_transformation('Счет 38976430693692818358') == 'Счет **8358'
