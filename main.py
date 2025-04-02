from GoogleDrive import GoogleDrive
from FileNameGenerator import FileNameGenerator

if __name__ == '__main__':
    # питание
    nutrition_empty_file_id = '1yjFeXLYGt5ApN6IFyJa24aKn_2e5QZMGr0QJ_17E080'
    # админы
    # TODO

    date_range = FileNameGenerator().get_date_range(
        start_date='01.04.2025',
        end_date='07.04.2025',
        include_days=[0, 1, 2, 3, 4]  # с пн по пт
    )
    print(date_range)

    d = GoogleDrive()
    # d.print_all_files()
    scripts_folder_id = d.create_folder('scripts')
    # copy_file_id = d.copy_file_to_folder(nutrition_empty_file_id, scripts_folder_id, 'file_name')
    # d.update_permissions(copy_file_id)
    for file_name in date_range:
        copy_file_id = d.copy_file_to_folder(nutrition_empty_file_id, scripts_folder_id, file_name)
        d.update_permission(copy_file_id)
