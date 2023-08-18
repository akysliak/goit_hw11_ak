"""
This is the main script of the application.

Notes:
    Possible commands: call "help" to get the command list and info
    The format of phone numbers and emails is checked with a very
        simple strategy, warning appears if the input does not pass validation
    Command "store" stores the current address books in the folder "users"
        in the same directory (will be created if does not exist),
        in a file <username>.bin
    Recognition of the commands is case-insensitive,
        the arguments are treated with respect to their case
        (e.g. name "ann" != "Ann")
    Provided arguments which are irrelevant for the specified command
        will be ignored (the command will be executed)

Possible improvements:
    improve format checking of the phone numbers/emails
    extend 'add' command: to allow multiple phones and emails to be provided
    improve storing and printing of the objects
"""

from addressbook import *
import os
import warnings

ADDRESSBOOK = AddressBook()
WARNING_COLOR = '\033[93m'  # '\033[92m' #'\033[93m'
RESET_COLOR = '\033[0m'

IDX_STRING = "idx="
INSTRUCTION_CHANGE = "\t<name> -n <new_name>\t-\tto change the contact name from its current value\n" \
                     "\t\t\t\t\t\t\t\t<name> to the value <new_name>\n" \
                     f"\t<name> [+p|+e] <phone|email> ({IDX_STRING}[first|last|<idx>])\t-\tto add a new\n" \
                     "\t\t\t\t\t\t\t\tphone number (+p <phone>) or e-mail (+e <email>)\n" \
                     "\t\t\t\t\t\t\t\tto the record with the name <name>,\n" \
                     f"\t\t\t\t\t\t\t\tOPTIONALLY: at the specified position ({IDX_STRING}) -\n" \
                     "\t\t\t\t\t\t\t\tat the beginning (first), end (last), specific index\n" \
                     "\t\t\t\t\t\t\t\t(<idx> starting with 1)\n" \
                     f"\t<name> [-p|-e] [<phone|email>|{IDX_STRING}[first|last|<idx>]]\t-\tto remove a phone\n" \
                     "\t\t\t\t\t\t\t\tnumber (-p) or an e-mail (-e)\n" \
                     "\t\t\t\t\t\t\t\tfrom the record with the name <name>,\n" \
                     "\t\t\t\t\t\t\t\tspecifying the target phone number/e-mail by its value\n" \
                     f"\t\t\t\t\t\t\t\t(<phone|email>) or position ({IDX_STRING}) in the record - at the\n" \
                     "\t\t\t\t\t\t\t\tbeginning (first), end (last), specific index\n" \
                     "\t\t\t\t\t\t\t\t(<idx> starting with 1)\n" \
                     f"\t<name> [edit-p|edit-e] [<phone|email>|{IDX_STRING}[first|last|<idx>]] <new_phone|email>\t-\n" \
                     "\t\t\t\t\t\t\t\tto edit a phone number (edit-p) or an e-mail (edit-e)\n" \
                     "\t\t\t\t\t\t\t\tin the record with the name <name> (replace an old value\n" \
                     "\t\t\t\t\t\t\t\twith the new value <new_phone|email>),\n" \
                     "\t\t\t\t\t\t\t\tspecifying the target phone number/e-mail by its value\n" \
                     f"\t\t\t\t\t\t\t\t(<phone|email>) or position ({IDX_STRING}) in the record - at the\n" \
                     "\t\t\t\t\t\t\t\tbeginning (first), end (last), specific index\n" \
                     "\t\t\t\t\t\t\t\t(<idx> starting with 1)"

INSTRUCTION_FIND = "\t-n <name>\t-\tto find the record with the contact name <name>\n" \
                   "\t-p <phone>\t-\tto find the record(s) with the phone number <phone>\n" \
                   "\t-e <email>\t-\tto find the record(s) with the e-mail <email>"

HELP_STRING = "This programme supports the following commands\n" \
              "(elements in () are optional, [] specify options to select from):\n" \
              "1.\tGreeting:\n" \
              "\thello\n" \
              "2.\tAdding new contact to the address book:\n" \
              "\tadd <name> (<phone> <email>)\n" \
              f"3.\tEditing existing contact in the address book:\n{INSTRUCTION_CHANGE}\n" \
              f"4.\tSearching for a record in the address book:\n{INSTRUCTION_FIND}\n" \
              "5.\tDeleting a contact from the address book:\n" \
              "\tdelete <name>\n" \
              "6.\tShowing all phone numbers saved for a given contact:\n" \
              "\tphone <name>\n" \
              "7.\tShowing all emails saved for a given contact:\n" \
              "\temail <name>\n" \
              "8.\tShowing all records in the address book:\n" \
              "\tshow all\n" \
              "9.\tShowing the username in the address book (the name of the owner):\n" \
              "\tusername\n" \
              "10.\tChanging the username in the address book:\n" \
              "\tnew username <username>\n" \
              "11.\tStoring current address book into a file (under the current username):\n" \
              "\tstore\n" \
              "12.\tLoading an address book from a file:\n" \
              "\tload <username>\n" \
              "13.\tExiting the programme:\n" \
              "\tgood bye\n" \
              "\tclose\n" \
              "\texit\n" \
              "14.\tGetting help:\n" \
              "\thelp\n" \
              "\nAll commands are case insensitive."


def hello_handler(*args):
    """
    Handles greeting.
    """
    return "How can I help you?"


def exit_handler(*args):
    """
    Handles programme performance by exiting.
    """
    return "Good bye!"


def add_handler(args):  # takes *arguments: 0-unlimited
    """
    Adds new contact to the address book.
    :param args: expected argument in the contact name.
    :return: confirmation that the new record with the specified contact name was added.
    """
    if len(args) < 1:
        raise ValueError("Give me a name for the new contact, please.")
    name = args[
        0]  # change to 1) args[0].title() if you want to always capitalize the 1st letter or to 2) args[0].lower().title()
    record = Record(name)

    phone = "NO PHONE NUMBER"
    email = "NO EMAIL"
    if len(args) > 1:
        phone = args[1]
        record.add_phone_number(phone)
    if len(args) > 2:
        email = args[2]
        record.add_email(email)
    ADDRESSBOOK.add_record(record)
    return f"New contact '{name}' with the phone number '{phone}' and email '{email}' successfully added."


def change_handler(args):
    """
    Changes existing contact in the address book.
    :param args: expects arguments which specify the change to be performed.
    :return: confirmation of the performed change.
    """
    if len(args) < 3 or (args[1].lower() not in ["-n", "+p", "+e", "-p", "-e", "edit-e", "edit-p"]) or \
            (args[1].lower() in ["edit-e", "edit-p"] and len(args) < 4):
        raise MyException(f"Please, specify the change parameters as follows:\n{INSTRUCTION_CHANGE}")
    param = args[1].lower()
    if param == "-n":
        change = Change(changetype=ChangeType.EDIT_NAME, name=args[0], new_name=args[2])
    elif param in ["+p", "+e"]:
        idx = None
        add_to_beginning = False
        if len(args) > 3:
            if args[3][len(IDX_STRING):].lower() == "first":
                add_to_beginning = True
            elif not args[3][len(IDX_STRING):].lower() == "last":
                idx = args[3][len(IDX_STRING):]
        changetype = ChangeType.ADD_PHONE if param == "+p" else ChangeType.ADD_EMAIL
        change = Change(changetype=changetype, name=args[0],
                        new_value=args[2], idx=idx,
                        add_to_beginning=add_to_beginning)  # new_value: str, idx = None, add_to_beginning = False
    else:
        cur_value = ""
        idx = None
        first = False
        last = False
        if not args[2].lower().startswith(IDX_STRING):
            cur_value = args[2]
        elif args[2][len(IDX_STRING):].lower() == "first":
            first = True
        elif args[2][len(IDX_STRING):].lower() == "last":
            last = True
        else:
            idx = args[2][len(IDX_STRING):]
        if param in ["-p", "-e"]:
            changetype = ChangeType.REMOVE_PHONE if param == "-p" else ChangeType.REMOVE_EMAIL
            change = Change(changetype=changetype, name=args[0],
                            cur_value=cur_value, idx=idx, first=first,
                            last=last)  # cur_value = "", idx = None, first = False, last = False
        else:
            new_value = args[3]
            changetype = ChangeType.EDIT_PHONE if param[-1] == "p" else ChangeType.EDIT_EMAIL
            change = Change(changetype=changetype, name=args[0],
                            new_value=new_value,
                            cur_value=cur_value, idx=idx, first=first,
                            last=last)  # self, new_value: str, cur_value="", idx=None, first=False, last=False
    record = ADDRESSBOOK.edit_record(change)
    return f"The record was successfully edited. Updated record:\n{record.to_string()}"


def find_handler(args):
    """
    Finds a record/records in the address book: by name, phone number or email.
    :param args: parameters to find the record(s).
    :return: the string representing the record(s).
    """
    if len(args) < 2 or args[0].lower() not in ["-n", "-p", "-e"]:
        raise MyException(f"Please, specify the search parameter, e.g.:\n{INSTRUCTION_FIND}")
    match args[0].lower():
        case "-n":
            param = "name"
            res = ADDRESSBOOK.get_record_by_name(args[1])
        case "-p":
            param = "phone number"
            res = ADDRESSBOOK.get_record_by_phone(args[1])
        case "-e":
            param = "e-mail"
            res = ADDRESSBOOK.get_record_by_email(args[1])
    if not res:
        return f"No record with the {param} '{args[1]}' found."
    elif type(res) == Record:
        return res.to_string()
    else:
        return "\n\n".join(record.to_string() for record in res)


def delete_handler(args):
    """
    Delets a contact from the address book.
    :param args: name of the contact for which the record should be deleted.
    :return: confirmation of the deletion.
    """
    if len(args) < 1:
        raise MyException("Please, give me the name of the contact to be deleted.")
    name = args[0]
    ADDRESSBOOK.delete_record(name)
    return f"The record for the name '{name} was successfully deleted."


def phone_handler(args):
    """
    Finds all phone numbers saved for a given contact.
    :param args: name of the contact whose phone number(s) has to be displayed.
    :return: phone number(s) of the specified contact (numerated if > 1).
    """
    if not args:
        raise ValueError("Please, enter the contact name.")
    name = args[0]
    record = ADDRESSBOOK.get_record_by_name(name)
    phones = record.get_phones()
    if len(phones) < 1:
        return f"no phones stored for {name}"
    if len(phones) == 1:
        return phones[0]
    return "\n".join(f"{position + 1}. {phone}" for position, phone in enumerate(phones))


def email_handler(args):
    """
    Finds all emails saved for a given contact.
    :param args: name of the contact whose email(s) has to be displayed.
    :return: email(s) of the specified contact (numerated if > 1).
    """
    if not args:
        raise ValueError("Please, enter the contact name.")
    name = args[0]
    record = ADDRESSBOOK.get_record_by_name(name)
    emails = record.get_emails()
    if len(emails) < 1:
        return f"no emails stored for {name}"
    if len(emails) == 1:
        return emails[0]
    return "\n".join(f"{position + 1}. {email}" for position, email in enumerate(emails))


def show_all_handler(*args):
    """
    Handles showing all records in the address book.
    :param args: no parameters expected.
    :return: string representing all the contacts in the address book.
    """
    res = ADDRESSBOOK.to_string()
    if not res:
        res = "Address book is empty."
    return res


def get_username_handler(args):
    """
    Gets current username in the address book (name of the address book owner).
    :param args: no parameters expected.
    :return: current username.
    """
    return ADDRESSBOOK.get_username()


def set_username_handler(args):
    """
    Changes the username in the address book (name of the address book owner).
    :param args: new username
    :return: confirmation that the username was changed.
    """
    if len(args) < 1:
        raise MyException("Please, specify the new user name.")
    name = args[0]
    ADDRESSBOOK.set_username(name)
    return f"The username successfully changed to '{name}'."


def store_handler(args):
    """
    Stores current address book into a binary file in the folder "users".
    By default, the current username will be used as the filename.
    :param args: not needed.
    :return: confirmation of the storage.
    """
    folder = "users"
    if folder not in os.listdir():
        os.makedirs(folder)
    ADDRESSBOOK.store_to_file(path=folder)
    return f"The address book for the user '{ADDRESSBOOK.get_username()}' was successfully stored."


def load_handler(args):
    """
    Loads an address book from a file. The must be in the folder "users" in the current directory.
    :param args: username whose address book has to be loaded.
    :return: confirmation of the loading.
    """
    if len(args) < 1:
        raise MyException("Please, specify the username.")
    name = args[0]
    filename = name + ".bin"
    folder = "users"
    if folder not in os.listdir() or filename not in os.listdir(folder):
        raise MyException(f"No address book stored for the user '{name}'")
    ADDRESSBOOK.load_from_file(os.path.join(folder, filename))
    return f"Address book for the user '{name}' successfully loaded."


def help_handler(args):
    return HELP_STRING


COMMANDS = {
    hello_handler: ["hello"],  # greeting
    add_handler: ["add"],  # adding new contact to the address book
    change_handler: ["change"],  # changing existing contact in the address book
    find_handler: ["find"],  # finding and showing a record in the address book: by name, phone number or email
    delete_handler: ["delete"],  # deleting a contact from the address book
    phone_handler: ["phone"],  # showing all phone numbers saved for a given contact
    email_handler: ["email"],  # showing all emails saved for a given contact
    show_all_handler: ["show all"],  # showing all records in the address book
    get_username_handler: ["username"],  # showing the username in the address book
    set_username_handler: ["new username"],  # changing the username in the address book
    store_handler: ["store"],  # storing current address book into a file
    load_handler: ["load"],  # loading an address book from a file
    exit_handler: ["good bye", "close", "exit"],  # exiting the programme
    help_handler: ["help"]  # getting help
}


def command_parcer(raw_str: str) -> (callable, list):
    case_insensitive = raw_str.lower()
    for handler, commands in COMMANDS.items():
        for command in commands:
            if case_insensitive == command or case_insensitive.startswith(command + " "):
                args = raw_str[len(command):].split()
                return handler, args
    return None, None


def input_error(fnc):
    def inner(*args):
        try:
            fnc(*args)
        except (IndexError, KeyError, ValueError, MyException) as e:
            print(str(e).replace('"', ""))
            inner()

    return inner


@input_error
def main():
    while True:
        u_input = input(">>> ")
        with warnings.catch_warnings(record=True) as warning_list:
            func, data = command_parcer(u_input)
            while not func:
                print("The command is not defined. Please, use a valid command")
                u_input = input(">>> ")
                func, data = command_parcer(u_input)
            result = func(data)
        for w in warning_list:
            print(f"\t{WARNING_COLOR}{w.message}{RESET_COLOR}")
        print(result)
        if func == exit_handler:
            break


if __name__ == "__main__":
    main()
