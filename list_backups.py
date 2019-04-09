from sys import argv

from config import load_config
from google_drive import list_files, build_service, get_credentials_from_config

load_config(argv[1])

google_api = build_service(get_credentials_from_config())

list_files(google_api)
