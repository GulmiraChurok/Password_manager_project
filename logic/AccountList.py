from data.Database import Database


class AccountList:
    __accounts = []
    __name = ""

    def __init__(self, name, security):
        self.__name = name
        self.__security = security
        self.__accounts = []

    def __iter__(self):
        return iter(self.__accounts)

    def add(self, account):
        if account not in self.__accounts:
            self.__accounts.append(account)

    def __add__(self, other):
        new_list = AccountList(self.get_name() + "/" + other.get_name(),
                               (int(self.get_security()) + int(other.get_security()))/2)
        for account in self:
            if account not in new_list:
                new_list.add(account)
        for account in other:
            if account not in new_list:
                new_list.add(account)
        return new_list

    def __str__(self):
        return F"{self.__name}: {self.__accounts}"

    def __repr__(self):
        return F"{self.__name}: {self.__accounts}"

    def get_name(self):
        return self.__name

    def get_security(self):
        return self.__security

    def get_key(self):
        return self.__name.lower()

    def to_dict(self):
        return {
            "_id": self.get_key(),
            "name": self.get_name(),
            "security": self.get_security(),
            "accounts": [account.get_key() for account in self.__accounts]
        }

    def remove(self, account):
        self.__accounts.remove(account)

    @staticmethod
    def read_account_lists():
        return Database.read_account_lists()

    def add_to_database(self):
        Database.add_account_list_to_database(self)

    def remove_from_database(self):
        Database.remove_account_list_from_database(self)