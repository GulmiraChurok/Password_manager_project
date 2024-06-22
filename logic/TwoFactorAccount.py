from logic.Account import Account


class TwoFactorAccount(Account):
    # def authenticate (self, type, info):
    def __init__(self, web_name, url, username, password, date_last_changed, auth_type, info):
        super().__init__(web_name, url, username, password, date_last_changed)
        self.auth_type = auth_type
        self.info = info

    def get_auth_type(self):
        return self.auth_type

    def get_info(self):
        return self.info

    def to_dict(self):
        return {
            "_id": self.get_key(),
            "type": "TwoFactorAccount",
            "web_name": self.get_name(),
            "url": self.get_url(),
            "username": self.get_username(),
            "password": self.get_password(),
            "date_last_changed": self.get_date_last_changed(),
            "auth_type": self.get_auth_type(),
            "info": self.get_info()
        }
