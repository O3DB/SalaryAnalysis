import os
import logging

from dotenv import load_dotenv
from requests.exceptions import HTTPError, ConnectionError

from hh import analyze_hh_vacancies
from superjob import analyze_sj_vacancies
from tools import print_ascii_table_for_salaries


load_dotenv()
SJ_API_KEY = os.getenv('SJ_API_KEY')

KEYWORDS = ['Python', 'Java', 'Javascript', 'C++']

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='my_script.log'
                    )
logger = logging.getLogger(__name__)     


def main():
    logger.info('Program started')
    try:
        print_ascii_table_for_salaries(analyze_hh_vacancies(KEYWORDS), 'HeadHunter Moscow')
        logger.info('Analytics table for HH successfully created')
        print('\n')
        print_ascii_table_for_salaries(analyze_sj_vacancies(KEYWORDS, SJ_API_KEY), 'SuperJob Moscow')
        logger.info('Analytics table for SJ successfully created')
    except (HTTPError, ConnectionError) as error:
        logger.error(error)


if __name__ == '__main__':
    main()