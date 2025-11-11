import logging

from decorators.http_errors import handle_http_errors
from src.GoogleDrive import GoogleDrive


def print_all_files(drive, folder_id='root', indent=0, indent_tab=4):
    results = drive.service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields="nextPageToken, files(id, name, mimeType)",
        pageSize=1000
    ).execute()

    items = results.get("files", [])
    for item in items:
        print(f"{' ' * indent}{item['mimeType']} | '{item['name']}' ({item['id']})")
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            print_all_files(drive, item['id'], indent + indent_tab)


if __name__ == '__main__':
    drive = GoogleDrive()
    print_all_files(drive)
