from json import dumps

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.client import Credentials

from config import get_config
from model import Quota


def get_credentials_from_config():
    credentials_string = dumps(get_config()['credentials'])
    return Credentials.new_from_json(credentials_string)


def build_service(creds):
    return build('drive', 'v3', credentials=creds, cache_discovery=False)


def get_quota(service):
    quota = service.about().get(fields="storageQuota").execute()
    return Quota.from_quota_response(quota)


def upload_file(service, path, remote_name):
    file_meta = {"name": remote_name}
    media = MediaFileUpload(path, resumable=True)
    media.stream()
    result = service.files().create(body=file_meta, media_body=media, fields="id").execute()
    return result
