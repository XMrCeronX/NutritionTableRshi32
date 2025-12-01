# NutritionTableRshi32
Скрипт для создания таблиц по питанию


git clone https://github.com/XMrCeronX/NutritionTableRshi32.git
 
зайти на

https://console.cloud.google.com/welcome/new

Создать проект, выбрать вновь созданный проект

В поиске найти "APIs & Services" и перейти во вкладку "Credentials"

Создать "OAuth 2.0 Client IDs" и "Service Accounts"

Create service account:
Задать имя, роль - owner

Create OAuth client ID:
To create an OAuth client ID, you must first configure your consent screen
Нужно настроить согласие нажав на кнопку создания проекта!
Нас перекидывает в Project configuration. Заполняем данные. Готово.

Заново заходим в "Create OAuth client ID" и создаем "Desktop app". 
После создания клиента вылезает окно в котором нужно скачать JSON файл.
Переименовать файл в "credentials.json" и добавить в проект.

После перейти в Google Auth Platform / Audience
найти и нажать кнопку Publish app.

Запускаем файл main.py. Заходим в аккаунт.
Даем доступ приложению:
"""Приложению "APP" нужны права доступа 
к вашему аккаунту Google"""

После должны получить сообщение:

"The authentication flow has completed. 
You may close this window."

Возможная ошибка:
Encountered 403 Forbidden with reason "accessNotConfigured".

Тогда нужно перейти в 
Google Cloud Console → APIs & Services → Library
найти и включить "Google Drive API" и "Google Sheets API" (ENABLE)

Создать файлы с таблицами. Берем ссылку. Пример:
https://docs.google.com/spreadsheets/d/1Ah4-3-To8o2Hn4rAy8o9L6_etitAfn86/edit?gid=1953053157#gid=1953053157
забираем от туда ID файла - "1Ah4-3-To8o2Hn4rAy8o9L6_etitAfn86"
и вставляем в конфиг и меняем NUTRITION_FILE_ID. 
Аналогично с ADMIN_FILE_ID.

! При добавлении создании файлов, стоит учесть что таблицу 
нужно сохранять как Google Таблицу, а не как .xlsx файл! 
Или же просто сохранить как Google таблицу: 

Файл -> Сохранить как таблицу Google + изменить NUTRITION_FILE_ID 
ADMIN_FILE_ID для соответствующих файлов

Иначе будет ошибка: 
gspread.exceptions.APIError: APIError: [400]: This operation is not supported for this document

Поменять почту в WRITER_ACCESS_EMAILS для Service Account
Пример:
noname@pure-iris-479510-u3.iam.gserviceaccount.com

Зайти в Credentials найти созданный Service Accounts. 
Нажать на него и зайти во вкладку Keys и добавить ключ JSON. 
Скачается файл, преименовать его в "service_account.json" и добавить в проект.
Пример JSON:
  "type": "service_account",
  "project_id": "*****",
  "private_key_id": "*****",
  "private_key": "*****",
  "client_email": "noname@pure-iris-479510-u3.iam.gserviceaccount.com",
  ......

Полезные материалы:
https://www.youtube.com/watch?v=xLHS8zIfTQo

TODO:
Добавить проверку есть ли файлы из конфига