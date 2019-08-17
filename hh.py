import os
from itertools import count
from statistics import mean

import requests

from tools import predict_salary


def get_hh_vacancies(keyword: str):
    '''get list of vacancies from HH API by keyword
    for Moscow region
    '''
    url = 'https://api.hh.ru/vacancies'
    vacancies = []

    for page in count(0):
        payload = {
        'text': keyword,
        'area': 1,
        'period': 30,
        'page': page,
        }
        response = requests.get(url, params=payload)
        if not response.ok or page >= response.json()['pages']:
            break
        vacancies.extend(response.json()['items'])

    return vacancies


def predict_hh_salary(vacancy):
    if not vacancy['salary']:
        return None

    salary_info = vacancy['salary']
    if salary_info['currency'] != 'RUR':
        return None

    return predict_salary(
        salary_from=salary_info['from'], 
        salary_to=salary_info['to']
        )


def analyze_hh_vacancies(keywords: list):
    '''Takes list of jobs_descriptions (keywords),
    get list of vacancies for each keyword from HH
    and returns dictionary with salary analytics (mean salary)
    '''
    result = dict()
    for keyword in keywords:
        vacancies = get_hh_vacancies(keyword)
        salaries = []
        for vacancy in vacancies:
            salary = predict_hh_salary(vacancy)
            if not salary:
                continue
            salaries.append(salary)
            result[keyword] = {
                "vacancies_found": len(vacancies),
                "vacancies_processed": len(salaries),
                "average_salary": int(mean(salaries))
            }
    return result