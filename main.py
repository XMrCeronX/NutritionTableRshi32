import logging

from gspread import service_account

from src.FileNameGenerator import FileNameGenerator
from src.GoogleDrive import GoogleDrive
from config import Config

logFormatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)-5.5s]: %(message)s.")
rootLogger = logging.getLogger()
rootLogger.setLevel(Config.DEBUG_LEVEL)

fileHandler = logging.FileHandler(Config.LOG_FILE_NAME, 'a', Config.LOG_ENCODING)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)


def update_cell_to_file_name(
        dict_files,
        cell_name='B1',
        default_worksheet=0
):
    gc = service_account(filename=Config.SERVICE_ACCOUNT_FILE_NAME)
    for dict_ in dict_files:
        for file_name, file_id in dict_.items():
            ss = gc.open_by_key(file_id)
            ws = ss.get_worksheet(default_worksheet)
            ws.update_acell(cell_name, file_name)
            logging.info(f'In file ({file_id}) {cell_name} updated to \'{file_name}\'')


if __name__ == '__main__':

    file_name_generator = FileNameGenerator()
    drive = GoogleDrive()
    data = []

    # =============== Для питания ===============
    nutrition_date_range = file_name_generator.get_date_range(
        start_date=Config.START_DATE,
        end_date=Config.END_DATE,
        include_days=Config.NUTRITION_INCLUDE_DAYS
    )
    logging.info(nutrition_date_range)
    nutrition_folder_id = drive.create_folder(Config.NUTRITION_FOLDER)
    for file_name in nutrition_date_range:
        copy_file_id = drive.copy_file_to_folder(
            Config.NUTRITION_FILE_ID,
            nutrition_folder_id,
            file_name,
            data
        )
        drive.update_permission(
            copy_file_id,
            emails=Config.WRITER_ACCESS_EMAILS
        )

    # =============== Для админов ===============
    admin_date_range = file_name_generator.get_date_range(
        start_date=Config.START_DATE,
        end_date=Config.END_DATE,
        include_days=Config.ADMIN_INCLUDE_DAYS
    )
    logging.info(admin_date_range)
    admin_folder_id = drive.create_folder(Config.ADMIN_FOLDER)
    for file_name in admin_date_range:
        copy_file_id = drive.copy_file_to_folder(
            Config.ADMIN_FILE_ID,
            admin_folder_id,
            file_name
        )
        drive.update_permission(
            copy_file_id,
            emails=Config.WRITER_ACCESS_EMAILS
        )

    logging.info(data)
    update_cell_to_file_name(data)
