from json import dumps, loads
from sys import argv

from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow, Credentials
from oauth2client.tools import argparser

from config import get_config, save_config, load_config
from model import OAuthSettings


def authorize(config_path, app_settings_path):
    settings = OAuthSettings.load_from_file(app_settings_path)
    flow = OAuth2WebServerFlow(client_id=settings.client_id,
                               client_secret=settings.client_secret,
                               scope=settings.scope,
                               redirect_uri=settings.redirect_uri)

    auth_url = flow.step1_get_authorize_url()
    print("Go to %s and paste received code here:" % auth_url)
    code = input()
    credentials = flow.step2_exchange(code=code)

    credentials_dict = loads(credentials.to_json())
    get_config()['credentials'] = credentials_dict
    save_config(config_path)

    service = build_service(credentials)
    result = service.about().get(fields="user").execute()
    return {
        "user": result['user']['displayName'],
        "email": result['user']['emailAddress']
    }


def build_service(credentials):
    return build('drive', 'v3', credentials=credentials, cache_discovery=False)


def get_credentials_from_config():
    credentials_string = dumps(get_config()['credentials'])
    return Credentials.new_from_json(credentials_string)


def validate():
    credentials = get_credentials_from_config()
    service = build_service(credentials)
    result = service.about().get(fields="user").execute()
    print(result)


def _print_user_from_response(result):
    name = result['user']['displayName']
    email = result['user']['emailAddress']
    print("Obtained credentials for %s(%s)\nYou can use the app now." % (name, email))


def refresh_token_and_store(path):
    mutable_credentials = get_credentials_from_config()
    credentials_in_config = get_credentials_from_config()
    service = build_service(mutable_credentials)
    result = service.about().get(fields="user").execute()
    if not credentials_in_config.access_token == mutable_credentials.access_token:
        get_config()['credentials'] = loads(mutable_credentials.to_json())
        save_config(path)
        return True
    else:
        return False


if __name__ == "__main__":
    load_config(argv[1])
    authorize(argv[1], argv[2])
