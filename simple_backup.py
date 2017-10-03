import random
import string
from json import load, dump
from sys import argv
from zipfile import ZipFile, ZIP_DEFLATED
from os.path import join
from os import walk, path

import logging

logging.basicConfig(format='%(asctime)-15s [ %(name)s ] %(message)s', level=logging.WARN)
log = logging.getLogger("Cloud Hamster")
log.setLevel(logging.INFO)

CONFIG = {}


def load_config(path):
    with open(path) as file_handler:
        config = load(file_handler)
        log.info("Loaded config from %s file, %d entries" % (path, len(config)))
        return config


def save_config(path):
    with open(path, "w") as file_handler:
        dump(file_handler, CONFIG)
        log.info("Stored config to %s file, %d entries" % (path, len(CONFIG)))


def merge_config(path):
    config_in_file = load_config(path)
    config_merged = config_in_file.copy()
    config_merged.update(CONFIG)
    with open(path, "w") as file_handler:
        dump(config_merged, file_handler)
        log.info("Stored merged config to %s file, %d entries" % (path, len(CONFIG)))


def _generate_random_filename():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))


def _get_temp_file():
    return join(CONFIG['temp_directory'], "hamster_" + _generate_random_filename())


def compress_folder(path, output_file):
    with ZipFile(file=output_file, mode="w", compression=ZIP_DEFLATED) as zip_file:
        for root, directory, files in walk(path):
            for file in files:
                zip_file.write(filename=join(root, file),
                               arcname=join(root.replace(path, ""), file))


def validate_google_account():
    if not CONFIG.get('credentials'):
        raise Exception(
            "Credentials for Google Drive not set. Please run \"authorize_google_drive.py %s %s\" to obtain credentials" % (
                argv[1], "app.json"))


CONFIG = load_config(argv[1])
validate_google_account()

compress_folder(CONFIG['backup_directory'], _get_temp_file());
