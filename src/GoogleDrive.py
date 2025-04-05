import logging
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from decorators.http_errors import handle_http_errors


class GoogleDrive:
    def __init__(self, token_file="token.json", creds_file="credentials.json"):
        self.SCOPES = [
            'https://www.googleapis.com/auth/drive',
        ]
        self.service = self._authenticate(token_file, creds_file)

    def _authenticate(self, token_file, creds_file):
        creds = None
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_file, self.SCOPES)
                creds = flow.run_local_server(port=0)

            with open(token_file, "w") as token:
                token.write(creds.to_json())

        return build("drive", "v3", credentials=creds)

    @handle_http_errors()
    def print_all_files(self, folder_id='root', indent=0, indent_tab=4):
        results = self.service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken, files(id, name, mimeType)",
            pageSize=1000
        ).execute()

        items = results.get("files", [])
        for item in items:
            print(f"{' ' * indent}{item['mimeType']} | '{item['name']}' ({item['id']})")
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                self.print_all_files(item['id'], indent + indent_tab)

    @handle_http_errors()
    def create_folder(self, folder_name, parent_id='root'):
        logging.info(f'Creating folder with name \'{folder_name}\'...')
        # Проверка существования папки
        response = self.service.files().list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{parent_id}' in parents and trashed=false",
            fields="files(id, name)"
        ).execute()

        if response.get("files"):
            folder_id = response["files"][0]["id"]
            logging.info(f"Folder '{folder_name}' ({folder_id}) already exists.")
            return folder_id

        # Создание новой папки
        folder_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id]
        }

        folder = self.service.files().create(body=folder_metadata, fields="id").execute()
        logging.info(f"Folder '{folder_name}' ({folder['id']}) created.")
        return folder["id"]

    @handle_http_errors()
    def get_files(self, file_id, fields='*'):
        """
        * - all metadata
        :param file_id:
        :param fields:
        :return:
        """
        return self.service.files().get(
            fileId=file_id,
            fields=fields
        ).execute()

    @handle_http_errors()
    def copy_file_to_folder(self, file_id, folder_id, new_title=None, data=None):
        file = self.get_files(file_id, "name, mimeType")

        # Если не указано новое название, оставляем исходное
        if new_title is None:
            new_title = file["name"]

        copied_file = {
            "name": new_title,
            "parents": [folder_id]
        }

        result = self.service.files().copy(
            fileId=file_id,
            body=copied_file,
            fields="id, name"
        ).execute()

        logging.info(f"File '{file['name']}' copied to folder {folder_id} with name \'{new_title}\' ({result['id']})")
        if data is not None:
            data.append({f'{new_title}': result['id']})
        return result["id"]

    @handle_http_errors()
    def update_permission(self, file_id, role='writer', type_='anyone', emails=None):
        permission = self.service.permissions().create(
            fileId=file_id,
            body={
                'role': role,
                'type': type_,
            }
        ).execute()
        permission_id = permission.get('id')
        link_to_file = f'https://docs.google.com/spreadsheets/d/{file_id}/edit'
        result_strings = [f"Link ({permission_id}): {link_to_file}"]

        if emails:  # полный доступ по email
            for email in emails:
                self.service.permissions().create(
                    fileId=file_id,
                    body={
                        'role': role,
                        'type': 'user',
                        'emailAddress': email,
                    },
                    # без уведомления пользователя, иначе засрет почту
                    sendNotificationEmail=False,
                ).execute()
                result_strings.append(f'{email} ({role})')

        logging.info(' + '.join(result_strings))
