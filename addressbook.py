from collections import UserDict
from record import *
from change import *
import warnings
import pickle
import os
from myexception import *


class AddressBook(UserDict):
    """
    Class representing the address book.
    """

    def __init__(self, username="defaultuser"):
        """
        Initiates the AddressBook object.
        :param username: name of the owner of the address book.
        """
        super(AddressBook, self).__init__(self)
        self.username = username    # owner of the address book

    def get_username(self):
        return self.username

    def set_username(self, new_name):
        self.username = new_name

    def add_record(self, record: Record):
        """
        Adds a new record to the address book.
        :param record: new record to be added to the address book.
        :return: None.
        """
        if record.get_name() in self.data:
            warnings.warn(f"WARNING: the record for the contact '{record.get_name()}' gets overwritten.")
        self.data[record.get_name()] = record

    def delete_record(self, name: str):
        """
        Deletes a record from the address book.
        :param name: contact name stored in the record which has to be deleted.
        :return: None.
        """
        try:
            del self.data[name]
        except KeyError:
            raise MyException(f"The record for the contact '{name}' cannot be deleted: this name is not in the address book.")

    def edit_record_name(self, old_name: str, new_name: str):
        """
        Changes the contact name within a record. Updates the way the record is stored in the address book.
        :param old_name: old name stored in a record that has to be changed.
        :param new_name: new name to replace the old one.
        :return: None.
        """
        try:
            record = self.data.pop(old_name)
            record.set_name(new_name)
            self.add_record(record)
            return record
        except KeyError:
            raise MyException(f"Cannot change the name of a record: the name '{old_name}' is not in the address book.")

    def edit_record(self, change: Change):
        """
        Conducts changes specified by the Change object.
        :param change: object containing information about the change which has to be performed.
        :return: None.
        """
        name = change.get_name()
        changetype = change.get_changetype()
        kwargs = change.get_kwargs()
        record = self.get_record_by_name(name)
        match changetype:
            case ChangeType.EDIT_NAME:
                record = self.edit_record_name(old_name=name, new_name=kwargs["new_name"])
            case ChangeType.EDIT_PHONE:
                record.edit_phone_number(**kwargs)
            case ChangeType.EDIT_EMAIL:
                record.edit_email(**kwargs)
            case ChangeType.ADD_PHONE:
                record.add_phone_number(**kwargs)
            case ChangeType.ADD_EMAIL:
                record.add_email(**kwargs)
            case ChangeType.REMOVE_PHONE:
                record.remove_phone_number(**kwargs)
            case ChangeType.REMOVE_EMAIL:
                record.remove_email(**kwargs)
            case _:
                raise MyException("Change type is unknown.")
        return record

    def get_record_by_name(self, name: str):
        """
        Finds a record by the contact name in it.
        :param name: the name to look for in records.
        :return: a record with the specified name.
        """
        if name in self.data:
            return self.data[name]
        else:
            raise MyException(f"No record with the name '{name}' in the address book.")

    def get_record_by_phone(self, phone: str):
        """
        Finds all records where specified phone number is found.
        :param phone: phone number to look for in records.
        :return: list of records which contain the specified phone number.
        """
        res = []
        for record in self.data.values():
            if phone in record.get_phones():
                res.append(record)
        if not res:
            raise MyException(f"No record with the phone number '{phone}' in the address book.")
        return res

    def get_record_by_email(self, email: str):
        """
        Finds all records where specified e-mail is found.
        :param email: e-mail to look for in records.
        :return: list of records which contain the specified e-mail.
        """
        res = []
        for record in self.data.values():
            if email in record.get_emails():
                res.append(record)
        if not res:
            raise MyException(f"No record with the email '{email}' in the address book.")
        return res

    def store_to_file(self, path="", filename=""):
        if not filename:
            filename = self.username
        filename = os.path.join(path, filename + ".bin")
        with open(filename, "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def load_from_file(self, filename):
        try:
            with open(filename, "rb") as f:
                ab = pickle.load(f)
                self.data = ab.data
                self.username = ab.username
        except FileNotFoundError:
            raise MyException(f"Address book cannot be loaded from the file '{filename}: the file does not exist.")

    def to_string(self):
        res = "\n\n".join(f"{pos+1}. {record.to_string()}" for pos, record in enumerate(self.data.values()))
        return res

