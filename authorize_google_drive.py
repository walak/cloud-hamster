from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import argparser

from model import OAuthSettings
from json import dumps, loads, load, dump
from simple_backup import CONFIG, merge_config
from sys import argv


def authorize(config_path, app_settings_path):
    flags = argparser.parse_args(["--noauth_local_webserver"])
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
    CONFIG['credentials'] = credentials_dict
    merge_config(config_path)

    service = build('drive', 'v3', credentials=credentials, cache_discovery=False)
    result = service.about().get(fields="user").execute()
    return {
        "user": result['user']['displayName'],
        "email": result['user']['emailAddress']
    }


logged_user = authorize(argv[1], argv[2])
print("Obtained credentials for %s(%s)\nYou can use the app now." % (logged_user['user'],logged_user['email']))
