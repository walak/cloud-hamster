import logging
from json import dump, load

logging.basicConfig(format='%(asctime)-15s [ %(name)s ] %(message)s', level=logging.WARN)
log = logging.getLogger("Cloud Hamster")
log.setLevel(logging.INFO)

CONFIG = {}


def load_config(path):
    global CONFIG
    with open(path) as file_handler:
        config = load(file_handler)
        log.info("Loaded config from %s file, %d entries" % (path, len(config)))
        CONFIG = config


def save_config(path):
    with open(path, "w") as file_handler:
        dump(CONFIG, file_handler)
        log.info("Stored config to %s file, %d entries" % (path, len(CONFIG)))


def get_config():
    return CONFIG
