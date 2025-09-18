import logging

from src.GoogleDrive import GoogleDrive

if __name__ == '__main__':
    drive = GoogleDrive()
    drive.print_all_files()
    # from datetime import datetime, timedelta
    #
    #
    # def get_next_day(date_str):
    #     # Преобразуем строку с датой в объект datetime
    #     input_date = datetime.strptime(date_str, '%drive.%m.%Y')
    #     # Вычисляем следующий день
    #     next_day = input_date + timedelta(days=1)
    #     # Возвращаем следующий день в формате 'дд.мм.гггг'
    #     return next_day.strftime('%drive.%m.%Y')
    #
    #
    # # Пример использования
    # logging.info(get_next_day('30.04.2025'))  # Результат: 12.04.2025
