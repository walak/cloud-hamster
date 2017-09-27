from oauth2client.client import OAuth2WebServerFlow

from model import OAuthSettings

settings = OAuthSettings.load_from_file("app.json")

flow = OAuth2WebServerFlow(client_id=settings.client_id,
                           client_secret=settings.client_secret,
                           scope=settings.scope,
                           redirect_uri=settings.redirect_uri)

print("Go to %s and copy received key: " % flow.step1_get_authorize_url())
key = input()

credentials = flow.step2_exchange(code=key)

print("OK@")
