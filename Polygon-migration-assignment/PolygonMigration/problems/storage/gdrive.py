# problems/storage/gdrive.py
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from .base import StorageBackend

SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GoogleDriveStorage(StorageBackend):
    def __init__(self):
        creds = Credentials.from_service_account_file(
            os.environ['GDRIVE_SERVICE_ACCOUNT_JSON'],
            scopes=SCOPES
        )
        self.service = build('drive', 'v3', credentials=creds)
        self.root_folder_id = os.environ['GDRIVE_ROOT_FOLDER_ID']

    def _ensure_folder(self, name, parent_id):
        query = f"name='{name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = self.service.files().list(q=query).execute().get('files', [])
        if results:
            return results[0]['id']

        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        folder = self.service.files().create(body=file_metadata, fields='id').execute()
        return folder['id']

    def upload_file(self, local_path: str, remote_path: str):
        parts = remote_path.strip('/').split('/')
        parent_id = self.root_folder_id

        # Create folders
        for part in parts[:-1]:
            parent_id = self._ensure_folder(part, parent_id)

        file_metadata = {
            'name': parts[-1],
            'parents': [parent_id]
        }
        media = MediaFileUpload(local_path, resumable=True)
        self.service.files().create(body=file_metadata, media_body=media).execute()

    def delete_prefix(self, remote_prefix: str):
        # empty
        pass
