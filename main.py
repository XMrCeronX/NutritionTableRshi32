import logging

from gspread import service_account

from config import Config
from logs.logs import init_logging
from src.FileNameGenerator import FileNameGenerator
from src.GoogleDrive import GoogleDrive


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


def main():
    init_logging()

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


if __name__ == '__main__':
    main()
