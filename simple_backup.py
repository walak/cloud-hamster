import logging
from os import walk, remove
from os.path import join
from sys import argv
from zipfile import ZipFile, ZIP_DEFLATED

from config import load_config, get_config
from files import get_temp_file_path, get_temp_file, generate_backup_name
from google_drive import build_service, get_credentials_from_config, get_quota, upload_file, list_files, BACKUP_FILTER, \
    remove_file

logging.basicConfig(format='%(asctime)-15s [ %(name)s ] %(message)s', level=logging.WARN)
log = logging.getLogger("Cloud Hamster")
log.setLevel(logging.INFO)


def compress_folder(path, output_file):
    log.info("Compressing folder [ %s ] into [ %s ]" % (str(path), output_file))
    with ZipFile(file=output_file, mode="w", compression=ZIP_DEFLATED) as zip_file:
        for root, directory, files in walk(path):
            for file in files:
                zip_file.write(filename=join(root, file),
                               arcname=join(root.replace(path, ""), file))
                log.info("Compressed file [ %s ] into [ %s ]" % (join(root, file), join(root.replace(path, ""), file)))


def validate_google_account():
    if not get_config().get('credentials'):
        raise Exception(
            "Credentials for Google Drive not set. Please run \"authorize_google_drive.py %s %s\" to obtain credentials" % (
                argv[1], "app.json"))


def file_to_int(file):
    name = file['name']
    created_at = name.split("_")[1]
    return int(created_at)


def found_oldest_backups(files):
    sorted_files = sorted(files, key=lambda f: file_to_int(f), reverse=True)
    return sorted_files[10:]


def check_current_backups(service):
    result = list_files(service, filter=BACKUP_FILTER)
    number_of_backups = len(result['files'])
    if number_of_backups <= 10:
        log.info("Found [ %d ] previous backups" % number_of_backups)
    else:
        log.info("Found more than 10 backups... removing oldest copies")
        files_to_remove = found_oldest_backups(result['files'])
        for remote_file in files_to_remove:
            result = remove_file(service, remote_file['id'])
            print(result)


load_config(argv[1])

validate_google_account()

google_api = build_service(get_credentials_from_config())

quota = get_quota(google_api)

print(quota.to_pretty_string())

tmp_file = get_temp_file()
tmp_path = get_temp_file_path(tmp_file)

check_current_backups(google_api)

compress_folder(get_config()['backup_directory'], tmp_path)

backup_name = generate_backup_name(get_config()['backup_directory'])
log.info("Storing backup as [ %s ]" % backup_name)

upload_file(google_api, tmp_path, backup_name)

remove(tmp_path)
