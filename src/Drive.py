from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class Drive:
    def __init__(self, creds_file_name="mycreds.txt"):
        self.gauth = GoogleAuth()
        self.gauth.LoadCredentialsFile(creds_file_name)
        if self.gauth.credentials is None:
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            self.gauth.Refresh()
        else:
            self.gauth.Authorize()
        self.gauth.SaveCredentialsFile(creds_file_name)

        self.drive = GoogleDrive(self.gauth)

    def print_all_files(self, folder_id='root', indent=0, indent_tab=4):
        file_list = self.drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
        for file in file_list:
            logging.info(f"{' ' * indent}{file['mimeType']} | \'{file['title']}\' ({file['id']})")
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                self.print_all_files(file['id'], indent + indent_tab)

    def create_folder(self, folder_name: str):
        """

        :param folder_name:
        :return: exists or created folder id
        """
        file_list = self.drive.ListFile({
            'q': f"'root' in parents and mimeType='application/vnd.google-apps.folder' and title='{folder_name}' and trashed=false"}).GetList()

        if file_list:
            folder_id = file_list[0]['id']
            logging.info(f'Folder \'{folder_name}\' ({folder_id}) already exists on Google Drive.')
            return folder_id
        else:
            folder = self.drive.CreateFile({
                'title': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            })
            folder.Upload()
            folder_id = folder['id']
            logging.info(f'Folder \'{folder_name}\' ({folder_id}) was created on Google Drive.')
            return folder_id

    def copy_file_to_folder(self, file_id, folder_id):
        file = self.drive.CreateFile({'id': file_id})
        file.FetchMetadata()

        file.GetContentFile('temp_file')  # Save to a temporary file

        copied_file = self.drive.CreateFile({
            'title': file['title'],
            'parents': [{'id': folder_id}],
        })

        copied_file.SetContentFile('temp_file')
        copied_file.Upload()

        import os
        os.remove('temp_file')

        logging.info(f"File '{file['title']}' was copied to folder ID: {folder_id}")
