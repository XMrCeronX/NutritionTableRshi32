from gspread import service_account

from FileNameGenerator import FileNameGenerator
from GoogleDrive import GoogleDrive
from config.BaseConfig import Config


def update_nutrition_cell_to_file_name(data):
    gc = service_account(filename='service_account.json')
    for dict_ in data:
        for file_name, file_id in dict_.items():
            print(f'{file_id}\t{file_name}')

            wks = gc.open_by_key(file_id).get_worksheet(0)
            wks.update_acell('B1', file_name)
            print('Cell updated.')

            # Update a range of cells using the top left corner address
            # wks.update([[1, 2], [3, 4]], 'A1')

            # Or update a single cell
            # wks.update_acell('B1', '')
            #
            # # Format the header
            # wks.format('A1:B1', {'textFormat': {'bold': True}})


if __name__ == '__main__':

    data = []

    # =============== Для питания ===============
    date_range = FileNameGenerator().get_date_range(
        start_date='07.04.2025',
        end_date='11.04.2025',
        include_days=Config.INCLUDE_DAYS  # с пн по пт
    )
    print(date_range)

    d = GoogleDrive()
    scripts_folder_id = d.create_folder(Config.FOLDER)
    for file_name in date_range:
        copy_file_id = d.copy_file_to_folder(Config.NUTRITION_EMPTY_FILE_ID, scripts_folder_id, file_name, data)
        d.update_permission(copy_file_id, emails=Config.WRITER_ACCESS_EMAILS)

    # =============== Для админов ===============
    date_range = FileNameGenerator().get_date_range(
        start_date='07.04.2025',
        end_date='11.04.2025',
        include_days=[0, 1, 2, 3]  # с пн по чт
    )
    print(date_range)

    d = GoogleDrive()
    scripts_folder_id = d.create_folder(f'{Config.FOLDER}/admin')
    for file_name in date_range:
        copy_file_id = d.copy_file_to_folder('1JxhrhfgNIgq_B7pdh1pcznbWMOc9dpZNFUv5S8XLjXE', scripts_folder_id,
                                             file_name)
        d.update_permission(copy_file_id, emails=Config.WRITER_ACCESS_EMAILS)

    print(data)
    update_nutrition_cell_to_file_name(data)
