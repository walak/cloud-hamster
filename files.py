import random
import string
from datetime import datetime
from os.path import join

from config import get_config
from base64 import b64encode


def get_date():
    return datetime.today().strftime('%Y%m%d')


def str_to_base64(s):
    encoded = s.encode('utf-8')
    return b64encode(encoded).decode('utf-8')


def generate_random_filename(l=20):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(l))


def get_temp_file():
    return "hamster_" + generate_random_filename()


def get_temp_file_path(filename):
    return join(get_config()['temp_directory'], filename)


def generate_backup_name(path):
    return "backup_%s-%sarchive.zip" % (get_date(), str_to_base64(str(path)))
