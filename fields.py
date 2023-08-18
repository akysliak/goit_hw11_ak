import warnings
from datetime import datetime
from myexception import MyException


class Field():
    """
    Class representing a fild in a record of an address book.
    """
    # name of the object type
    name = "field"

    def __init__(self, value: str):
        self.value = value

    def set_value(self, new_value: str):
        self.value = new_value

    def get_value(self):
        return self.value

    def get_name(self):
        return self.name

    def validate(self, value: str):
        return True

    def __repr__(self):
        return f"{self.name}: {self.value}"


class Name(Field):
    """
    Class representing the contact name stored in a record of an address book.
    """
    def __init__(self, value: str):
        super(Name, self).__init__(value)
        self.name = "name"


class Phone(Field):
    """
    Class representing a phone number within a record of an address book.
    """
    def __init__(self, value: str):
        if self.validate(value):
            super(Phone, self).__init__(value)
            self.name = "phone"
        else:
            raise MyException(f"The value {value} is not a valid telephone number. Please, provide another value.")

    def validate(self, phone: str):
        """
        Conducts a simple check if the given phone number is well-formed. Raises WARNING if it is not.
        NB: not a full check, only spots some incorrect features.
        :param phone: the phone number to be checked.
        :return: True if the phone number passes the simple check.
        """
        if phone and phone.isdigit() or (len(phone)>2 and phone[0] == "+" and phone[1:].isdigit()):
            length = len(phone) -1 if phone[0] == "+" else len(phone)
            if length < 3 or length > 15:
                warnings.warn(f"WARNING: the phone number '{phone}' is potentially malformed.")
            return True
        return False

class Email(Field):
    """
    Class representing an email within a record of an address book.
    """
    def __init__(self, value: str):
        super(Email, self).__init__(value)
        self.validate(value)
        self.name = "e-mail"

    def validate(self, email: str):
        """
        Conducts a simple check if the given e-mail is well-formed. Raises WARNING if it is not.
        NB: not a full check, only spots some incorrect features.
        :param email: the e-mail to be checked.
        :return: True if the e-mail passes the simple check.
        """
        parts = email.split("@")
        if len(parts) == 2 and len(parts[1].split(".")) == 2:
            return True
        warnings.warn(f"WARNING: the email '{email}' is malformed.")


class Birthday(Field):
    """
    Class representing birthday info within a record of an address book.
    """
    def __init__(self, value: str):
        if self.validate(value):
            super(Birthday, self).__init__(value)
            self.name = "birthday"
        else:
            raise MyException(f"The value {value} is not a valid birthday value. Please, provide another value in the format 'dd/mm/yyyy.")

    def validate(self, value: str):
        date  = value.split("/")
        if len(date) > 2 and
            day, month,
        try:
            birthday = datetime.strptime(value, "%d/%m/%Y")
            print(birthday)
            return True
        except Exception as e:
            print(e)
            return False

if __name__ == "__main__":
    # testing validate() methods
    print(Email("shf_4uh@d.re"))
    print(Phone("+36785295720958"))
    print(Phone("+366"))
    #print(Phone("+36785295720958666827529"))
    print(Birthday("24/08/54"))



