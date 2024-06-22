from logic.AccountList import AccountList
from ui.input_validation import *
from logic.Account import Account
from logic.TwoFactorAccount import TwoFactorAccount
from datetime import datetime


class PasswordManager:
    __all_accounts = None
    __account_lists = []

    @classmethod
    def print_account_list(cls):
        names = [account_list.get_name() for account_list in cls.__account_lists]  # list comprehension
        choice = select_item("Please select an account list name to print accounts in it: ",
                             "Must be an account list name", choices=names)
        print(choice)
        account_list = cls.lookup_account_list(choice)
        print(F"These are the accounts in {choice} list: ")
        for account in account_list:
            print("    ", account)
            print()

    @classmethod
    def print_account_lists(cls):
        print("Current Account Lists: ")
        for account_list in cls.__account_lists:
            print("    ", account_list.get_name())

    @classmethod
    def init(cls):
        cls.__all_accounts, cls.__account_lists = cls.read_account_lists()

    @staticmethod
    def print_menu():
        print("Welcome to the password manager!")
        print("Choose an action:")
        print("     1. Show a list of current account lists.")
        print("     2. Create a new account list.")
        print("     3. Delete an account list.")
        print("     4. Select an account list and show the list of accounts in the list.")
        print("     5. Select an account list and add a new account to the list.")
        print("     6. Select an account list and remove an account from the list.")
        print("     7. Select an account by website and username(across all account lists)"
              " and update the password for that account.")
        print("     8. Join two account lists.")
        print("     9. Exit")

    @classmethod
    def create_new_account_list(cls):
        name = input_string("What is the name of the new account list? ")
        security = input_int("What is the security level for this account list? ",
                             "security_level must be a whole number between 0-10", ge=0, le=10)
        account_list = cls.lookup_account_list(name)
        if account_list is not None:
            print("This account list already exists!")
            return
        new_account_list = AccountList(name, security)
        AccountList.add_to_database(new_account_list)
        cls.__account_lists.append(new_account_list)

    @classmethod
    def lookup_account_list(cls, name):
        for account_list in cls.__account_lists:
            if account_list.get_name().lower() == name.lower():
                return account_list
        return None

    @classmethod
    def lookup_account(cls, web_name, username):
        for account in cls.__all_accounts:
            if account.get_name().lower() == web_name.lower() and account.get_username().lower() == username.lower():
                return account
        return None

    @classmethod
    def remove_account_list(cls):
        names = [account_list.get_name() for account_list in cls.__account_lists]  # list comprehension
        choice = select_item("Please select account list name you want to remove: ",
                             "Must be an account list name", choices=names)
        print(choice)
        account_list = cls.lookup_account_list(choice)
        if account_list is not None:   # is it redundant? with error message form choice we are getting the right accountlist name, so account list cannot be none?
            cls.__account_lists.remove(account_list)
            account_list.remove_from_database()

    @classmethod
    def remove_account(cls):
        names = [account_list.get_name() for account_list in cls.__account_lists]  # list comprehension
        choice = select_item("Please select account list name you want to remove from: ",
                             "Must be an account list name", choices=names)
        print(choice)
        account_list = cls.lookup_account_list(choice)
        if account_list.get_key() == "all accounts":
            print("You cannot remove an account from 'All Accounts' list")
            return
        web_name = input_string("What is website name of the account you want to remove: ")
        username = input_string("What is username of the account you want to remove: ")
        account = cls.lookup_account(web_name, username)
        if account is None:
            print("There is no such account!")
            return
        account_list.remove(account)
        account_list.add_to_database()

    @classmethod
    def add_new_account(cls):
        names = [account_list.get_name() for account_list in cls.__account_lists]  # list comprehension
        choice = select_item("Please select account list to add a new account: ",
                             "Must be an account list name", choices=names)
        print(choice)
        account_list = cls.lookup_account_list(choice)
        web_name = input_string("What is the name of the website? ")
        username = input_string("What is the username for this website? ")
        account = cls.lookup_account(web_name, username)
        if account is not None:
            print("This account already exists!")
            return
        is_two_factor_account = y_or_no("Does a new account have two factor authentication?")
        url = input_string("What is the URL of the website? ")
        password = input_string("What is the password for this website? ")
        date_last_changed = datetime.now()
        if is_two_factor_account:
            auth_type = input_string("What type of authentication to use: phone app, pin number or secret question? ")
            info = input_string("What is your information to authenticate? ")
            account = TwoFactorAccount(web_name, url, username, password, date_last_changed, auth_type, info)
            account_list.add(account)
            account.add_to_database()
            cls.__all_accounts.add(account)
            account_list.add_to_database()
            cls.__all_accounts.add_to_database()
            return
        account = Account(web_name, url, username, password, date_last_changed)
        account_list.add(account)
        account.add_to_database()
        cls.__all_accounts.add(account)
        account_list.add_to_database()
        cls.__all_accounts.add_to_database()

    @classmethod
    def update_password(cls):
        web_name = input_string("What is website name of the account you want to update password: ")
        username = input_string("What is username of that account: ")
        account = cls.lookup_account(web_name, username)
        if account is None:
            print("There is no such account!")
            return
        new_password = input_string("Please type a new password: ")
        account.change_password(new_password)
        account.add_to_database()

    @classmethod
    def join_lists(cls):
        names = [account_list.get_name() for account_list in cls.__account_lists]  # list comprehension
        choice1 = select_item("Please select first account list to join: ",
                              "Must be an account list name", choices=names)
        choice2 = select_item("Please select second account list to join: ",
                              "Must be an account list name", choices=names)
        account_list1 = cls.lookup_account_list(choice1)
        account_list2 = cls.lookup_account_list(choice2)
        new_list = account_list1 + account_list2
        cls.__account_lists.append(new_list)
        new_list.add_to_database()

    @staticmethod
    def read_account_lists():
        return AccountList.read_account_lists()

    @classmethod
    def run(cls):
        while True:
            cls.print_menu()
            choice = select_item("What would you like to do: ", "Answer must be 1,2,3,4,5,6,7,8,9",
                                 ["1", "2", "3", "4", "5", "6", "7", "8", "9"])
            print()
            if choice == "9":
                print("Good bye!")
                break
            elif choice == "1":
                cls.print_account_lists()
            elif choice == "2":
                cls.create_new_account_list()
            elif choice == "3":
                cls.remove_account_list()
            elif choice == "4":
                cls.print_account_list()
            elif choice == "5":
                cls.add_new_account()
            elif choice == "6":
                cls.remove_account()
            elif choice == "7":
                cls.update_password()
            elif choice == "8":
                cls.join_lists()
            print()



if __name__ == '__main__':      # what is it? why do we do it?
    # app = PasswordManager()
    # app.run()
    PasswordManager.init()
    PasswordManager.run()
    # PasswordManager.read_account_lists()
    # app.read_account_lists()



