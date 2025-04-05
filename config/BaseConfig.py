from abc import ABC


class BaseConfig(ABC):
    # =============== Для питания ===============
    # папка на google диске в которую все будет скопировано
    FOLDER = 'scripts'
    # список отдельных почт которым будте предоставлен полный доступ
    WRITER_ACCESS_EMAILS = []
    # ID файла с питанием
    NUTRITION_EMPTY_FILE_ID = '1yjFeXLYGt5ApN6IFyJa24aKn_2e5QZMGr0QJ_17E080'

    # =============== Для админов ===============
    # ID файла с админами
    # TODO
    # с пн по пт
    INCLUDE_DAYS = [0, 1, 2, 3, 4]


class Config(BaseConfig):
    FOLDER = 'scripts'
    WRITER_ACCESS_EMAILS = [
        'noname@my-project-test-455417.iam.gserviceaccount.com',  # сервис акк обязателен!
        'eabrsim@gmail.com'
    ]
