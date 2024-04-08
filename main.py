from src.config import config
from src.db_manager import DBManager
from src.hh_api import HHApi


def main(company_id=None):
    # Параметры подключения к БД
    my_db = config('src/database.ini')

    hh_api = HHApi()
    db_manager = DBManager(my_db)

    # Создание таблиц
    db_manager.create_tables()

    # Получение данных о компаниях и вакансиях
    companies = ["9498120", "9608107", "6146301", "1470975", "3870258", "3123738", "1060821", "10941115", "10530948", "10853846"]  # Замените на реальные идентификаторы компаний
    for company_id in companies:
        vacancies = hh_api.get_vacancies(company_id)
        if vacancies:
            db_manager.insert_data(vacancies)

    # Выполнение запросов к базе данных и обработка результатов
    companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
    all_vacancies = db_manager.get_all_vacancies()
    avg_salary = db_manager.get_avg_salary()
    vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
    vacancies_with_keyword = db_manager.get_vacancies_with_keyword("python")

    print("Companies and Vacancies Count:", companies_and_vacancies_count)
    print("All Vacancies:", all_vacancies)
    print("AVG salary:", avg_salary)
    print("Vacancies with higher salary:", vacancies_with_higher_salary)
    print("Vacancies with Keyword:", vacancies_with_keyword)


if __name__ == "__main__":
    main()