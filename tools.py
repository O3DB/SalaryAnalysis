from terminaltables import AsciiTable


def predict_salary(salary_from: int, salary_to: int) -> int:
    if salary_from and salary_to:
        return int((salary_from + salary_to) / 2)
    elif salary_from:
        return int(salary_from * 1.2)
    elif salary_to:
        return int(salary_to * 0.8)
    else: return None


def print_ascii_table_for_salaries(jobs_statistics: dict, title=None):
    table_data = [('Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата')]
    for job_title, statistic in jobs_statistics.items():
        table_data.append((job_title, statistic['vacancies_found'], statistic['vacancies_processed'], statistic['average_salary']))
    table = AsciiTable(table_data, title=title)
    print(table.table)
    