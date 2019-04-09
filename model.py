from json import load, dump


class Quota:
    def __init__(self, usage, limit, usage_in_trash, usage_in_drive):
        self.usage = usage
        self.limit = limit
        self.usage_in_trash = usage_in_trash
        self.usage_in_drive = usage_in_drive

    def usage_in_percents(self):
        return float(self.usage) / float(self.limit) * 100

    def limit_in_mb(self):
        return self.limit / 1024 / 1024

    def usage_in_mb(self):
        return self.usage / 1024 / 1024

    def usage_in_trash_in_mb(self):
        return self.usage_in_trash / 1024 / 1024

    def usage_in_drive_mb(self):
        return self.usage_in_drive / 1024 / 1024

    @classmethod
    def from_quota_response(cls, response):
        return cls(usage=int(response['storageQuota']['usage']),
                   limit=int(response['storageQuota']['limit']),
                   usage_in_trash=int(response['storageQuota']['usageInDriveTrash']),
                   usage_in_drive=int(response['storageQuota']['usageInDrive']))

    def to_pretty_string(self):
        return "Qouta summary(%.2f%% free):\n" \
               "Usage: %.2f MB\n" \
               "Usage (in Drive): %.2f MB\n" \
               "Limit: %.2f MB\n" \
               "In trash: %.2f MB" % (
                   self.usage_in_percents(),
                   self.usage_in_mb(),
                   self.usage_in_drive_mb(),
                   self.limit_in_mb(),
                   self.usage_in_trash_in_mb())


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

    def save_to_file(self, path):
        with open(path) as file:
            dump(self.to_dict(), path)

    @staticmethod
    def load_from_file(path):
        with open(path) as file:
            d = load(file)
            return OAuthSettings.from_dict(d)
