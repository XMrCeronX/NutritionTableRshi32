from datetime import datetime, timedelta


class FileNameGenerator:
    DEFAULT_DATE_FORMAT = '%drive.%m.%Y'

    def get_current_week(self, include_days=None):
        """
        Возвращает список дат текущей недели.

        :param include_days: Список дней недели для включения (0 - понедельник, 6 - воскресенье).
                             Например, [0, 1, 2] для понедельника, вторника и среды.
        :return: Список строк с датами в формате 'дд.мм.гггг'.
        """
        if include_days is None:
            include_days = [0, 1, 2, 3, 4, 5, 6]  # Включить все дни недели
        today = datetime.now()
        # Находим первый день недели (понедельник)
        start_of_week = today - timedelta(days=today.weekday())
        week_dates = []
        for i in range(7):  # Проходим по всем дням недели
            current_day = start_of_week + timedelta(days=i)
            if current_day.weekday() in include_days:
                week_dates.append(current_day.strftime(self.DEFAULT_DATE_FORMAT))

        return week_dates

    def get_date_range(self, start_date=None, end_date=None, include_days=None):
        """
        Возвращает список дат в указанном диапазоне.

        :param start_date: Дата начала диапазона в формате 'дд.мм.гггг'.
        :param end_date: Дата конца диапазона в формате 'дд.мм.гггг'.
        :param include_days: Список дней недели для включения (0 - понедельник, 6 - воскресенье).
                             Например, [0, 1, 2] для понедельника, вторника и среды.
        :return: Список строк с датами в формате 'дд.мм.гггг'.
        """
        if start_date is None:
            start_date = datetime.now().strftime(self.DEFAULT_DATE_FORMAT)

        if end_date is None:
            end_date = (datetime.now() + timedelta(days=7)).strftime(self.DEFAULT_DATE_FORMAT)

        if include_days is None:
            include_days = [0, 1, 2, 3, 4, 5, 6]  # Включить все дни недели

        start_date_obj = datetime.strptime(start_date, self.DEFAULT_DATE_FORMAT)
        end_date_obj = datetime.strptime(end_date, self.DEFAULT_DATE_FORMAT)

        date_range = []

        current_date = start_date_obj
        while current_date <= end_date_obj:
            if current_date.weekday() in include_days:
                date_range.append(current_date.strftime(self.DEFAULT_DATE_FORMAT))
            current_date += timedelta(days=1)

        return date_range
