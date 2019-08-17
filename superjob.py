import os
import pprint
from itertools import count
from statistics import mean

import requests
from dotenv import load_dotenv

from tools import predict_salary


load_dotenv()

SJ_API_KEY = os.getenv('SJ_API_KEY')


KEYWORDS = ['Python', 'Java', 'Javascript', 'C++', 'DWDM', 'базовые станции']

def get_sj_vacancies(keyword: str, api_key: str):
    url = 'https://api.superjob.ru/2.0/vacancies'
    vacancies = []
    headers = {
        'X-Api-App-Id': api_key
    }
    for page in count(0):
        params = {
            'town': 4,
            'keyword': keyword,
            'page': page,
        }
        response = requests.get(url, headers=headers, params=params)
        if not response.ok:
            break
        vacancies.extend(response.json()['objects'])
        if not response.json()['more']:
            break
    return vacancies

def predict_sj_salary(vacancy):
    if vacancy['currency'] != 'rub':
        return None
    return predict_salary(
        salary_from=vacancy['payment_from'], 
        salary_to=vacancy['payment_to']
        )


def analyze_sj_vacancies(keywords: list, api_key: str):
    result = dict()
    for keyword in keywords:
        vacancies = get_sj_vacancies(keyword, api_key)
        salaries = []
        for vacancy in vacancies:
            salary = predict_sj_salary(vacancy)
            if not salary:
                continue
            salaries.append(salary)
            result[keyword] = {
                "vacancies_found": len(vacancies),
                "vacancies_processed": len(salaries),
                "average_salary": int(mean(salaries))
            }
    return result


if __name__ == '__main__':
    res = analyze_sj_vacancies(keywords=KEYWORDS, api_key=SJ_API_KEY)
    pprint.pprint(res)