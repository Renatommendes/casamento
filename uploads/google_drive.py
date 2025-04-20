# uploads/google_drive.py

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SERVICE_ACCOUNT_FILE = 'credencial.json'  # caminho da sua chave
FOLDER_ID = '1wBUCgc5hGkSbhfbbeNhAURCIEcEdpQrl'

def upload_to_drive(file_path, filename):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': filename,
        'parents': [FOLDER_ID]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()

    return file.get('webViewLink')
