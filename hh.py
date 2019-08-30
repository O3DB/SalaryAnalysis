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
        
        response_json = response.json()
        vacancies.extend(response_json['items'])
        if page_num >= response_json['pages'] - 1:
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
    result = dict()
    for keyword in keywords:
        vacancies = get_hh_vacancies(keyword)
        salaries = []
        for vacancy in vacancies:
            salary = predict_hh_salary(vacancy)
            if not salary:
                continue
            salaries.append(salary)

            #add job analytics to resulting dict
            #keyword is a job_description
            result[keyword] = {
                "vacancies_found": len(vacancies),
                "vacancies_processed": len(salaries),
                "average_salary": int(mean(salaries))
            }
    return result