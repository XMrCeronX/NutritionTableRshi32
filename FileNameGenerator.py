from datetime import datetime, timedelta


class FileNameGenerator:

    @staticmethod
    def get_current_week(include_days=None):
        """
        Возвращает список дат текущей недели.

        :param include_days: Список дней недели для включения (0 - понедельник, 6 - воскресенье).
                             Например, [0, 1, 2] для понедельника, вторника и среды.
        :return: Список строк с датами в формате 'дд.мм.гггг'.
        """
        if include_days is None:
            include_days = [0, 1, 2, 3, 4, 5, 6]  # Включить все дни недели

        # Получаем текущую дату
        today = datetime.now()

        # Находим первый день недели (понедельник)
        start_of_week = today - timedelta(days=today.weekday())

        # Создаем список дат
        week_dates = []

        for i in range(7):  # Проходим по всем дням недели
            current_day = start_of_week + timedelta(days=i)
            if current_day.weekday() in include_days:
                week_dates.append(current_day.strftime('%d.%m.%Y'))

        return week_dates

    @staticmethod
    def get_date_range(start_date=None, end_date=None, include_days=None):
        """
        Возвращает список дат в указанном диапазоне.

        :param start_date: Дата начала диапазона в формате 'дд.мм.гггг'.
        :param end_date: Дата конца диапазона в формате 'дд.мм.гггг'.
        :param include_days: Список дней недели для включения (0 - понедельник, 6 - воскресенье).
                             Например, [0, 1, 2] для понедельника, вторника и среды.
        :return: Список строк с датами в формате 'дд.мм.гггг'.
        """
        if start_date is None:
            start_date = datetime.now().strftime('%d.%m.%Y')

        if end_date is None:
            end_date = (datetime.now() + timedelta(days=7)).strftime('%d.%m.%Y')

        if include_days is None:
            include_days = [0, 1, 2, 3, 4, 5, 6]  # Включить все дни недели

        # Преобразуем даты в datetime объекты
        start_date_obj = datetime.strptime(start_date, '%d.%m.%Y')
        end_date_obj = datetime.strptime(end_date, '%d.%m.%Y')

        # Создаем список дат
        date_range = []

        current_date = start_date_obj
        while current_date <= end_date_obj:
            if current_date.weekday() in include_days:
                date_range.append(current_date.strftime('%d.%m.%Y'))
            current_date += timedelta(days=1)

        return date_range

    # # Пример использования
    # current_week_dates = get_current_week(include_days=[0, 1, 2, 3])  # Включить понедельник по четверг
    # print(current_week_dates)
