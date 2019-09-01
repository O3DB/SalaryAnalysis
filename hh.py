import os
from itertools import count
from statistics import mean

import requests

from tools import predict_salary


def get_hh_vacancies(keyword: str):
    """Get list of vacancies from HH API by keyword for Moscow region"""
    url = 'https://api.hh.ru/vacancies'
    vacancies = []
    moscow_area_code = 1
    time_period_days = 30

    for page_num in count(0):
        payload = {
        'text': keyword,
        'area': moscow_area_code,
        'period': time_period_days,
        'page': page_num,
        }
        response = requests.get(url, params=payload)
        response.raise_for_status()
        
        hh_data = response.json()
        vacancies.extend(hh_data['items'])
        if page_num >= hh_data['pages'] - 1:
            break

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
    """Takes list of jobs_descriptions (keywords),
    get list of vacancies for each keyword from HH
    and returns dictionary with salary analytics (mean salary)
    """
    import time
    start_time = time.time()
    result = dict()
    for keyword in keywords:
        vacancies = get_hh_vacancies(keyword)
        salaries = [predict_hh_salary(vacancy) for vacancy in vacancies]
        salaries = [salary for salary in salaries if salary]

        result[keyword] = {
            "vacancies_found": len(vacancies),
            "vacancies_processed": len(salaries),
            "average_salary": int(mean(salaries))
            }
    return result