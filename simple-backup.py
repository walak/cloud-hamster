from json import load
from sys import argv

CONFIG = {}


def load_config(path):
    with open(path) as file_handler:
        config = load(file_handler)
        return config

CONFIG = load_config(argv[1])

