import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class DriveAPI:
    def __init__(self, token_file="token.json", creds_file="credentials.json"):
        self.SCOPES = [
            'https://www.googleapis.com/auth/drive',
            # 'https://spreadsheets.google.com/feeds',
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

    def print_all_files(self, folder_id='root', indent=0, indent_tab=4):
        try:
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

        except HttpError as error:
            print(f"An error occurred: {error}")

    def create_folder(self, folder_name, parent_id='root'):
        print(f'Creating folder with name \'{folder_name}\'...')
        try:
            # Проверка существования папки
            response = self.service.files().list(
                q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{parent_id}' in parents and trashed=false",
                fields="files(id, name)"
            ).execute()

            if response.get("files"):
                folder_id = response["files"][0]["id"]
                print(f"Folder '{folder_name}' ({folder_id}) already exists.")
                return folder_id

            # Создание новой папки
            folder_metadata = {
                "name": folder_name,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [parent_id]
            }

            folder = self.service.files().create(body=folder_metadata, fields="id").execute()
            print(f"Folder '{folder_name}' ({folder['id']}) created.")
            return folder["id"]

        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def get_files(self, file_id, fields='*'):
        """
        * - all metadata
        :param file_id:
        :param fields:
        :return:
        """
        try:
            return self.service.files().get(
                fileId=file_id,
                fields=fields
            ).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def copy_file_to_folder(self, file_id, folder_id, new_title=None):
        try:
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

            print(f"File '{file['name']}' copied to folder {folder_id} with name \'{new_title}\' ({result['id']})")
            return result["id"]

        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def update_permission(self, file_id, role='writer', type_='anyone'):
        try:
            permission = self.service.permissions().create(
                fileId=file_id,
                body={
                    'role': role,
                    'type': type_,
                }
            ).execute()
            permission_id = permission.get('id')
            # print(f"Permission ID: {permission_id}")
            # print(f"FILE: https://drive.google.com/file/d/{file_id}/edit")
            link_to_file = f'https://docs.google.com/spreadsheets/d/{file_id}/edit'
            print(f"Link ({permission_id}): {link_to_file}")
        except Exception as e:
            print(f"An error occurred: {e}")
