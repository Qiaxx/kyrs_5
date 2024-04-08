import requests


class HHApi:
    def __init__(self):
        pass

    def get_vacancies(self, company_id):
        response = requests.get(f"https://api.hh.ru/vacancies?employer_id={company_id}&per_page=100")
        if response.status_code == 200:
            return response.json()
        else:
            return None
