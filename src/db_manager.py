import psycopg2


class DBManager:
    def __init__(self, db_con):
        self.conn = psycopg2.connect(**db_con)
        self.cur = self.conn.cursor()

    def create_tables(self):
        create_companies_table = """
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            vacancies_count INTEGER
        )
        """
        create_vacancies_table = """
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            company_id INTEGER REFERENCES companies(id),
            name VARCHAR(255) NOT NULL,
            salary VARCHAR(100),
            link VARCHAR(255)
        )
        """
        self.cur.execute(create_companies_table)
        self.cur.execute(create_vacancies_table)
        self.conn.commit()

    def insert_data(self, data):
        for vacancy in data['items']:
            company_id = vacancy['employer']['id']
            company_name = vacancy['employer']['name']
            vacancies_count = len(vacancy)
            vacancy_name = vacancy['name']
            salary = vacancy['salary']['to'] if vacancy['salary'] else None
            link = vacancy['alternate_url']

            insert_company_query = """
            INSERT INTO companies (id, name, vacancies_count)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """
            self.cur.execute(insert_company_query, (company_id, company_name, vacancies_count))

            insert_vacancy_query = """
            INSERT INTO vacancies (company_id, name, salary, link)
            VALUES (%s, %s, %s, %s)
            """
            self.cur.execute(insert_vacancy_query, (company_id, vacancy_name, salary, link))

        self.conn.commit()

    def get_companies_and_vacancies_count(self):
        query = """
        SELECT name, vacancies_count FROM companies
        """
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_all_vacancies(self):
        query = """
        SELECT c.name AS company_name, v.name AS vacancy_name, v.salary, v.link 
        FROM vacancies v 
        INNER JOIN companies c ON v.company_id = c.id
        """
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_avg_salary(self):
        query = """
        SELECT AVG(CAST(REPLACE(salary, ' ', '') AS INTEGER)) AS avg_salary FROM vacancies WHERE salary IS NOT NULL
        """
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        query = """
        SELECT c.name AS company_name, v.name AS vacancy_name, v.salary, v.link 
        FROM vacancies v 
        INNER JOIN companies c ON v.company_id = c.id
        WHERE CAST(REPLACE(salary, ' ', '') AS INTEGER) > %s
        """
        self.cur.execute(query, (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        query = """
        SELECT c.name AS company_name, v.name AS vacancy_name, v.salary, v.link 
        FROM vacancies v 
        INNER JOIN companies c ON v.company_id = c.id
        WHERE LOWER(v.name) LIKE %s
        """
        self.cur.execute(query, ('%' + keyword.lower() + '%',))
        return self.cur.fetchall()
