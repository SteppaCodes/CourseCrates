from decouple import config
from gdstorage.storage import GoogleDriveStorage, _ANYONE_CAN_READ_PERMISSION_
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import json


class CustomGoogleDriveStorage(GoogleDriveStorage):
    def __init__(self, permissions=None):
        # Use decouple to retreive the environment variable instead of os.environ
        credentials = Credentials.from_service_account_info(
            json.loads(config("GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE_CONTENTS")),
            scopes=['https://www.googleapis.com/auth/drive'],
        )
        self._permissions = [_ANYONE_CAN_READ_PERMISSION_]
        self._drive_service = build('drive', 'v3', credentials=credentials)