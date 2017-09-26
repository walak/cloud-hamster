import random
import string
from json import load
from sys import argv
from zipfile import ZipFile, ZIP_DEFLATED
from os.path import join
from os import walk, path

CONFIG = {}


def load_config(path):
    with open(path) as file_handler:
        config = load(file_handler)
        return config


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


CONFIG = load_config(argv[1])

compress_folder(CONFIG['backup_directory'], _get_temp_file());
