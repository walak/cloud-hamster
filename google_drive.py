import logging
from json import dumps

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.client import Credentials

from config import get_config
from model import Quota

log = logging.getLogger("Google Drive")
log.setLevel(logging.INFO)

BACKUP_FILTER = 'name contains "backup_" and mimeType="application/zip"'


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


def remove_file(service, file_id):
    result = service.files().delete(fileId=file_id).execute()
    return result


def list_files(service, filter):
    files = service.files().list(q=filter).execute()
    return files
