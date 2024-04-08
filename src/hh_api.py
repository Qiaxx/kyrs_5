import requests


class HHApi:
    def __init__(self):
        """
        Инициализатор класса подключения к hh.ru
        """
        pass

    def get_vacancies(self, company_id):
        """
        Метод получения вакансий по идентификатору компании
        :param company_id: идентификатор компании
        :return: json файл с вакансиями компании
        """
        response = requests.get(f"https://api.hh.ru/vacancies?employer_id={company_id}&per_page=100")
        if response.status_code == 200:
            return response.json()
        else:
            return None
