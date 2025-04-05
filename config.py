import logging


class Config():
    # Google sheets:
    SERVICE_ACCOUNT_FILE_NAME = 'service_account.json'
    START_DATE = '07.04.2025'
    END_DATE = '11.04.2025'
    # logging
    LOG_FILE_NAME = 'log.log'
    DEBUG_LEVEL = logging.INFO
    LOG_ENCODING = 'UTF-8'

    # Google Drive API:
    # список отдельных почт которым будет предоставлен полный доступ
    WRITER_ACCESS_EMAILS = [
        'noname@my-project-test-455417.iam.gserviceaccount.com',  # сервис акк обязателен!
        'eabrsim@gmail.com'
    ]
    # =============== Для питания ===============
    # папка на google диске в которую все будет скопировано
    NUTRITION_FOLDER = 'scripts'
    # ID файла с питанием
    NUTRITION_FILE_ID = '1yjFeXLYGt5ApN6IFyJa24aKn_2e5QZMGr0QJ_17E080'
    NUTRITION_INCLUDE_DAYS = [0, 1, 2, 3, 4]  # с пн по пт

    # =============== Для админов ===============
    # папка на google диске в которую все будет скопировано
    ADMIN_FOLDER = f'{NUTRITION_FOLDER}/admin'
    # ID файла с питанием
    ADMIN_FILE_ID = '1JxhrhfgNIgq_B7pdh1pcznbWMOc9dpZNFUv5S8XLjXE'
    ADMIN_INCLUDE_DAYS = [0, 1, 2, 3]  # с пн по чт
