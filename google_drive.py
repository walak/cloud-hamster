from json import dumps
from sys import argv

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.client import Credentials

from simple_backup import load_config, CONFIG


def get_credentials_from_config():
    credentials_string = dumps(CONFIG['credentials'])
    return Credentials.new_from_json(credentials_string)


def build_service(credentials):
    return build('drive', 'v3', credentials=credentials, cache_discovery=False)


if __name__ == "__main__":
    load_config(argv[1])
    credentials = get_credentials_from_config()
    service = build_service(credentials)
    file_meta = {"name": "to_be_removed.bmp"}
    media = MediaFileUpload('file-2560.bmp', mimetype='image/bmp', resumable=True)
    media.stream()
    result = service.files().create(body=file_meta, media_body=media, fields="id").execute()
    print(result)
