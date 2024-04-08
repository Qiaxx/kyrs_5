from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    """
    Функция для получения параметров для подключения к БД
    :param filename: название файла (по умолчанию database.ini)
    :param section: позиция, под которой ищет параметры для подключения (по умолчанию postgresql)
    :return: переменную db с параметрами (dbname=dbname, host=host, user=user, password=password, port=port)
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
