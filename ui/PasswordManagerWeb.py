from flask import Flask, render_template, request, redirect, url_for
from logic.AccountList import AccountList


class PasswordManagerWebUI:
    __app = Flask(__name__)
    __all_accounts = None
    __account_lists = None

    @classmethod
    def init(cls):
        cls.__app.secret_key = "some string value"
        cls.__all_accounts, cls.__account_lists \
            = cls.read_account_lists()

    @staticmethod
    def find_account_list(account_list_name):
        for account_list in PasswordManagerWebUI.__account_lists:
            if account_list.get_key() == account_list_name.lower():
                return account_list
        return None

    @staticmethod
    def find_account(account_name, account_list):
        for account in account_list:
            if account_name.lower() == account.get_key().lower():
                return account
        return None

    @staticmethod
    def read_account_lists():
        return AccountList.read_account_lists()

    @staticmethod
    @__app.route("/print_account_lists")
    def print_account_lists():
        return render_template('print_account_lists.html', account_lists=PasswordManagerWebUI.__account_lists)

    @staticmethod
    @__app.route("/select_account_list_for_print")
    def select_account_list_for_print():
        return render_template('select_account_list_for_print.html',
                               account_lists=PasswordManagerWebUI.__account_lists)

    @staticmethod
    @__app.route("/select_account_list_for_delete")
    def select_account_list_for_delete():
        return render_template('select_account_list_for_delete.html',
                               account_lists=PasswordManagerWebUI.__account_lists)

    @staticmethod
    @__app.route("/print_account_list")
    def print_account_list():
        account_list_name = request.args["account_list_name"]
        for account_list in PasswordManagerWebUI.__account_lists:
            if account_list.get_key() == account_list_name.lower():
                return render_template("print_account_list.html", account_list=account_list)
        return render_template("error.html",
                                   error_message=F"Error! Couldn't find an account list named {account_list_name}!")

    @staticmethod
    @__app.route("/delete_account_list")
    def delete_account_list():
        if "account_list_name" not in request.args:
            return render_template("error.html",
                                   error_message=F"Error! No valid account name is specified.")
        account_list_name = request.args["account_list_name"]
        for account_list in PasswordManagerWebUI.__account_lists:
            if account_list.get_key() == account_list_name.lower():
                PasswordManagerWebUI.__account_lists.remove(account_list)
                account_list.remove_from_database()
                return render_template("delete_succeeded.html", account_list_name=account_list_name)
        return render_template("error.html",
                                error_message=F"Error! Couldn't find an account list named {account_list_name}!")

    @staticmethod
    @__app.route("/get_account_password_for_update")
    def get_account_password_for_update():
        return render_template('get_account_password_for_update.html',
                               all_accounts=PasswordManagerWebUI.__all_accounts)

    @staticmethod
    @__app.route("/update_password", methods=["GET", "POST"])
    def update_password():
        if "account_name" not in request.form:
            return render_template("error.html",
                                   error_message=F"Error! No valid account name is specified.")
        account_key = request.form["account_name"]
        if "password" not in request.form:
            return render_template("error.html",
                                   error_message=F"Error! No valid password is specified.")
        password = request.form["password"]
        for account in PasswordManagerWebUI.__all_accounts:
            if account_key == account.get_key():
                account.change_password(password)
                account.add_to_database()
                return render_template("update_succeeded.html", account_name=account.get_name(), password=password)
        return render_template("error.html",
                               error_message=F"Error! Couldn't find an account named {account_key}!")

    @staticmethod
    @__app.route("/select_account_for_remove")
    def select_account_for_remove():
        account_list_name = request.args["account_list_name"]
        account_list = PasswordManagerWebUI.find_account_list(account_list_name)
        if account_list is None:
            return render_template("error.html",
                                   error_message=F"Error! Couldn't find account list {account_list_name}!")
        return render_template("select_account_for_remove.html", account_list=account_list)

    @staticmethod
    @__app.route("/select_account_list_for_remove_account")
    def select_account_list_for_remove_account():
        return render_template("select_account_list_for_remove_account.html",
                               account_lists=PasswordManagerWebUI.__account_lists)

    @staticmethod
    @__app.route("/remove_account_from_list")
    def remove_account_from_list():
        account_name = request.args["account_name"]
        account_list_name = request.args["account_list_name"]
        account_list = PasswordManagerWebUI.find_account_list(account_list_name)
        if account_list is None:
            return render_template("error.html",
                                   error_message=F"Error! Couldn't find account list {account_list_name}!")
        account = PasswordManagerWebUI.find_account(account_name, account_list)
        if account is None:
            return render_template("error.html",
                                   error_message=F"Error! Couldn't find account named {account_name} in list {account_list_name}!")
        account_list.remove(account)
        account_list.add_to_database()
        return render_template("remove_account_from_list_succeeded.html",
                               account_name=account_name, account_list_name=account_list_name)

    @staticmethod
    @__app.route("/type_account_list_for_add")
    def type_account_list_for_add():
        return render_template('type_account_list_for_add.html')

    @staticmethod
    @__app.route("/add_account_list")
    def add_account_list():
        if "account_list_name" not in request.args:
            return render_template("error.html",
                                   error_message=F"Error! No valid account name is specified.")
        name = request.args["account_list_name"]
        if "security" not in request.args:
            return render_template("error.html",
                                   error_message=F"Error! No valid security level is specified.")
        security = request.args["security"]

        for account_list in PasswordManagerWebUI.__account_lists:
            if account_list.get_name().lower() == name.lower():
                return render_template("error.html",
                                       error_message=F"Error! Account List {name} already exists!")
        account_list = AccountList(name, security)
        AccountList.add_to_database(account_list)
        PasswordManagerWebUI.__account_lists.append(account_list)
        return render_template("add_account_list_succeeded.html", account_list_name=name)

    @staticmethod
    @__app.route("/select_account_lists_for_join")
    def select_account_lists_for_join():
        return render_template("select_account_lists_for_join.html", account_lists=PasswordManagerWebUI.__account_lists)

    @staticmethod
    @__app.route("/join_account_lists")
    def join_account_lists():
        account_list_name_1 = request.args["account_list_name_1"]
        account_list_name_2 = request.args["account_list_name_2"]
        account_list_1 = PasswordManagerWebUI.find_account_list(account_list_name_1)
        account_list_2 = PasswordManagerWebUI.find_account_list(account_list_name_2)
        if account_list_1 is None:
            return render_template("error.html",
                                   error_message=F"Error! Couldn't find account list {account_list_name_1}!")
        if account_list_2 is None:
            return render_template("error.html",
                                   error_message=F"Error! Couldn't find account list {account_list_name_2}!")
        new_list = account_list_1 + account_list_2
        PasswordManagerWebUI.__account_lists.append(new_list)
        new_list.add_to_database()
        return render_template("join_succeeded.html",
                               account_list_name_1=account_list_name_1, account_list_name_2=account_list_name_2)


    @staticmethod
    @__app.route("/")
    def redirect_to_main():
        return redirect(url_for("main_menu"))

    @staticmethod
    @__app.route("/main_menu")
    def main_menu():
        return render_template("main_menu.html")

    @classmethod
    def run(cls):
        PasswordManagerWebUI.__app.run(port=8000)

if __name__ == "__main__":
    PasswordManagerWebUI.init()
    PasswordManagerWebUI.run()

