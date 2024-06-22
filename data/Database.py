from pymongo import *


class Database:
    __client = None
    __password_manager = None
    __accounts_collection = None
    # __two_factor_accounts_collection = None
    __account_list_collection = None

    @classmethod
    def __connect(cls):
        if cls.__client is None:
            cls.__client = MongoClient("mongodb+srv://gulmirachurokova:python2@cluster0.8hocyzw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
            cls.__password_manager = cls.__client.PasswordManager
            cls.__accounts_collection = cls.__password_manager.Accounts
            # cls.__two_factor_accounts_collection = db.TwoFactorAccounts
            cls.__account_list_collection = cls.__password_manager.AccountList

    @classmethod
    def rebuild_data(cls):
        cls.__connect()
        cisco = {
            "_id": "cisco guma",
            "type": "Account",
            "web_name": "Cisco",
            "url": "www.cisco.com",
            "username": "guma",
            "password": "abc123",
            "date_last_changed": "02/20/2024"
        }
        facebook = {
            "_id": "facebook puma",
            "type": "Account",
            "web_name": "Facebook",
            "url": "www.facebook.com",
            "username": "puma",
            "password": "abc124",
            "date_last_changed": "02/20/2024"
        }
        dance = {
            "_id": "dance luma",
            "type": "Account",
            "web_name": "Dance",
            "url": "www.dance.com",
            "username": "luma",
            "password": "abc125",
            "date_last_changed": "02/20/2024"
        }
        cook = {
            "_id": "cook ruma",
            "type": "TwoFactorAccount",
            "web_name": "Cook",
            "url": "www.cook.com",
            "username": "ruma",
            "password": "abc126",
            "date_last_changed": "02/20/2024",
            "authentication_type": "pin",
            "info": "1204"
        }
        cls.__accounts_collection.drop()
        cls.__account_list_collection.drop()
        cls.__accounts_collection = cls.__password_manager.Accounts
        cls.__account_list_collection = cls.__password_manager.AccountList

        result = cls.__accounts_collection.insert_many([cisco, facebook, dance, cook])
        cls.__account_list_collection.insert_one({
            "_id": "all accounts",
            "name": "All Accounts",
            "security": "2",
            "accounts": [account["_id"] for account in [cisco, facebook, dance, cook]]
        })
        cls.__account_list_collection.insert_one({
            "_id": "work",
            "name": "work",
            "security": "3",
            "accounts": [account["_id"] for account in [cisco, cook]]
        })
        cls.__account_list_collection.insert_one({
            "_id": "home",
            "name": "home",
            "security": "8",
            "accounts": [account["_id"] for account in [facebook, dance]]
        })

    @classmethod
    def dump_data(cls):
        cls.__connect()
        accounts = cls.__accounts_collection.find()
        for account in accounts:
            print(account)
        account_lists = cls.__account_list_collection.find()
        for account_list in account_lists:
            print(account_list)

    @classmethod
    def read_account_lists(cls):
        from logic.Account import Account
        from logic.TwoFactorAccount import TwoFactorAccount
        from logic.AccountList import AccountList
        cls.__connect()
        accounts = cls.__accounts_collection.find()
        account_objects = []
        for account_dict in accounts:
            if account_dict["type"] == "Account":
                account_objects.append(Account(
                    account_dict["web_name"],
                    account_dict["url"],
                    account_dict["username"],
                    account_dict["password"],
                    account_dict["date_last_changed"]
                ))
            elif account_dict["type"] == "TwoFactorAccount":
                account_objects.append(TwoFactorAccount(
                    account_dict["web_name"],
                    account_dict["url"],
                    account_dict["username"],
                    account_dict["password"],
                    account_dict["date_last_changed"],
                    account_dict["type"],
                    account_dict["info"]
                ))
            else:
                print("Invalid account: ", account_dict)

        account_map = {}
        for account in account_objects:
            account_map[account.get_key()] = account

        account_lists = cls.__account_list_collection.find()
        all_lists = []
        all_accounts = None
        for account_list_dict in account_lists:
            account_list = AccountList(account_list_dict["name"], account_list_dict["security"])
            for account_key in account_list_dict["accounts"]:
                account_list.add(account_map[account_key])
            all_lists.append(account_list)
            if account_list.get_name() == "All Accounts":
                all_accounts = account_list
        return all_accounts, all_lists

    @classmethod
    def add_account_list_to_database(cls, new_account_list):
        cls.__connect()
        # cls.__account_list_collection.insert_one(new_account_list.to_dict())
        cls.__account_list_collection.update_one({"_id": new_account_list.get_key()},
                                                 {"$set": new_account_list.to_dict()}, upsert=True)

    @classmethod
    def add_account_to_database(cls, account):
        cls.__connect()
        # cls.__accounts_collection.insert_one(account.to_dict())
        cls.__accounts_collection.update_one({"_id": account.get_key()}, {"$set": account.to_dict()}, upsert=True)

    @classmethod
    def remove_account_list_from_database(cls, account_list):
        # cls.__connect() #do i need it here?
        cls.__account_list_collection.delete_one({"_id": account_list.get_key()})


