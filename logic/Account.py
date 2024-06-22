from datetime import datetime
from data.Database import Database


class Account:
    __web_name = ""
    __url = ""
    __username = ""
    __password = ""
    __date_last_changed = ""

    def __init__(self, web_name, url, username, password, date_last_changed):
        self.__web_name = web_name
        self.__url = url
        self.__username = username
        self.__password = password
        self.__date_last_changed = date_last_changed

    def __str__(self):
        return "Web Name: " + self.__web_name + "\n     username: " + self.__username

    def __repr__(self):
        return "Web Name: " + self.__web_name + "\n     username: " + self.__username

    def change_password(self, new_password):
        self.__password = new_password
        self.__date_last_changed = datetime.now()

    def get_name(self):
        return self.__web_name

    def get_url(self):
        return self.__url

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_date_last_changed(self):
        return self.__date_last_changed

    def get_key(self):
        return F"{self.__web_name} {self.__username}".lower()

    def add_to_database(self):
        Database.add_account_to_database(self)

    def to_dict(self):
        return {
            "_id": self.get_key(),
            "type": "Account",
            "web_name": self.get_name(),
            "url": self.get_url(),
            "username": self.get_username(),
            "password": self.get_password(),
            "date_last_changed": self.get_date_last_changed()
        }
