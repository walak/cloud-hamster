from json import load


class OAuthSettings:
    def __init__(self, client_id, client_secret, scope, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.redirect_uri = redirect_uri

    def to_dict(self):
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": self.scope,
            "redirect_uri": self.redirect_uri
        }

    @classmethod
    def from_dict(cls, d):
        return cls(client_id=d['client_id'],
                   client_secret=d['client_secret'],
                   scope=d['scope'],
                   redirect_uri=d['redirect_uri'])

    @staticmethod
    def load_from_file(path):
        with open(path) as file:
            d = load(file)
            return OAuthSettings.from_dict(d)
