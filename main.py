import os

from dotenv import load_dotenv

from hh import analyze_hh_vacancies
from superjob import analyze_sj_vacancies
from tools import print_ascii_table_for_salaries


load_dotenv()

SJ_API_KEY = os.getenv('SJ_API_KEY')

KEYWORDS = ['Python', 'Java', 'Javascript', 'C++']
        

def main():
    print_ascii_table_for_salaries(analyze_hh_vacancies(KEYWORDS), 'HeadHunter Moscow')
    print('\n')
    print_ascii_table_for_salaries(analyze_sj_vacancies(KEYWORDS, SJ_API_KEY), 'SuperJob Moscow')


if __name__ == '__main__':
    main()