import requests
import pprint
from statistics import mean
from itertools import count

def hh(job_description):
    url = 'https://api.hh.ru/vacancies'
    payload = {
        'text': job_description,
        'area': 1,
        'period': 30
        }
    response = requests.get(url, params=payload)
    return response.json()['found']


def get_python_salaries():
    url = 'https://api.hh.ru/vacancies'
    payload = {
        'text': 'python',
        'area': 1,
        'period': 30
        }
    response = requests.get(url, params=payload)
    for item in response.json()['items']:
        print(item['salary'])


def predict_rub_salary(job_title):
    vacancies, vacancies_found = get_vacancies(job_title)
    url = 'https://api.hh.ru/vacancies'
    
    salaries = []
    vacancies_processed = 0
    for vacancy in vacancies:
        if not vacancy['salary']:
            continue
        salary_info = vacancy['salary']
        if salary_info['currency'] != 'RUR':
            continue
        elif salary_info['from'] and salary_info['to']:
            salaries.append((salary_info['from'] + salary_info['to'])/2)  
            vacancies_processed += 1          
        elif salary_info['from']:
            salaries.append(salary_info['from'] * 1.2)
            vacancies_processed += 1
        else:
            salaries.append(salary_info['to'] * 0.8)
            vacancies_processed += 1
    average_salary = int(mean(salaries))

    return {
        "vacancies_found": vacancies_found,
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }

def get_vacancies(job_title):
    url = 'https://api.hh.ru/vacancies'
    vacancies = []
    for page in count(0):
        payload = {
        'text': job_title,
        'area': 1,
        'period': 30,
        'page': page,
        }
        response = requests.get(url, params=payload)
        # response.raise_for_status()
        if not response.ok or page >= response.json()['pages']:
            break

        vacancies.extend(response.json()['items'])
        found = response.json()['found']
    
    return vacancies, found
    # pprint.pprint(vacancies[0])
        

def main():
    jobs = ['python', 'java', 'javascript', 'базовые станции', 'DWDM', 'e-commerce']
    jobs_info = {}
    for job in jobs:
        jobs_info[job] = predict_rub_salary(job)
    pprint.pprint(jobs_info)

if __name__ == '__main__':
    # vacancies, found = get_vacancies('python')
    # pprint.pprint(vacancies)
    # print(found)
    main()
    # get_vacancies('базовые станции')