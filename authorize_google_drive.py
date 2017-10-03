from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import argparser

from model import OAuthSettings
import httplib2

settings = OAuthSettings.load_from_file("app.json")

flow = OAuth2WebServerFlow(client_id=settings.client_id,
                           client_secret=settings.client_secret,
                           scope=settings.scope,
                           redirect_uri=settings.redirect_uri)

flags = argparser.parse_args(["--noauth_local_webserver"])

auth_url = flow.step1_get_authorize_url()

print("Go to %s and paste received code here:" % auth_url)
code = input()

credentials = flow.step2_exchange(code=code)
transport = httplib2.Http()

service = build('drive', 'v3', credentials=credentials)
result = service.about().get(fields="storageQuota").execute()
print(result)