import json


def get_db_state():
    """
    get database state
    :return: database state
    """
    return json.load(open('app/config/config.json', encoding='utf-8'))['reset_db']


def get_csv_files():
    """
    get dictionary of csv files
    :return: dictionary of csv files
    """
    return json.load(open('app/config/config.json', encoding='utf-8'))['csv_files']


def get_list_of_countries():
    """
    get list of countries
    :return: list of countries
    """
    return json.load(open('app/config/config.json', encoding='utf-8'))['countries']
