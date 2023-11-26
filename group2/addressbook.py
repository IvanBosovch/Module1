from pathlib import Path
from collections import UserDict
from collections.abc import Iterator
from datetime import datetime
import pickle

import re


class Field:
    def __init__(self):
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self):
        super().__init__()
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    def __str__(self):
        return self.__value


class Phone(Field):
    def __init__(self, value):
        super().__init__()
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if len(new_value) != 10 or not new_value.isdigit():
            raise ValueError
        self.__value = new_value


class Birthday(Field):
    def __init__(self):
        super().__init__()
        self.__value = "unknown"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: datetime):
        if type(new_value) != datetime:
            raise ValueError
        else:
            self.__value = new_value.date()


class Email(Field):
    def __init__(self):
        super().__init__()
        self.__value = "no email"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: str):
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", new_value):
            raise ValueError("Check mail format")
        self.__value = new_value
    
    def __str__(self):
        return self.__value
    
    def __len__(self):
        return len(self.__value) 

class Address(Field):
    def __init__(self):
        super().__init__()
        self.__value = "no address"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: str):
        self.__value = new_value
    
    def __len__(self):
        return len(self.__value) 


class Record:
    def __init__(self, name: Name):
        new_name = Name()
        new_name.value = name
        self.name = new_name
        self.phones = []
        self.birthday = Birthday()
        self.email = Email()
        self.address = Address()

    def add_phone(self, phone):
        new_phone = Phone(phone)
        if not phone in "".join(p.value for p in self.phones):
            new_phone.value = phone
            self.phones.append(new_phone)

    def remove_phone(self, phone: str):
        self.phones.remove(self.find_phone(phone))

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        new_ph = Phone(new_phone)
        new_ph.value = new_phone
        self.phones.append(new_ph)

    def find_phone(self, phone: str):
        for x in self.phones:
            if x.value == phone:
                return x

    def add_birthday(self, birthday):
        self.birthday.value = birthday

    def add_email(self, email):
        self.email.value = email

    def add_address(self, address):
        self.address.value = address

    def days_to_birthday(self):
        today = datetime.now().date()
        if today < self.birthday.value.replace(year=today.year):
            next_bd = self.birthday.value.replace(year=today.year)
            days_to_bd = next_bd - today
            return days_to_bd.days
        elif today == self.birthday.value.replace(year=today.year):
            next_bd = self.birthday.value.replace(year=today.year)
            days_to_bd = next_bd - today
            return f"\033[31mtoday\033[0m"
        else:
            next_bd = self.birthday.value.replace(year=today.year + 1)
            days_to_bd = next_bd - today
            return days_to_bd.days
        


    def __str__(self):
        from service_addressbook import longest_params
        longest = longest_params()
        print (longest['name'])
    
        start_line = "\u250d" + "\u2500" * longest['sum'] + "\u2511" + "\n"
        phone_fuller = "  \u2502{: <44}\u2502{: <39}\u2502{: <72}\u2502\n\u2502{: >30}\u2502{: >9}".format(
            " ", " ", " ", " ", " "
        )
        separation_line = "\n\u2515" + "\u2500" * longest['sum'] + "\u2519" + "\n"

        if (
            self.birthday.value != "unknown"
            and self.days_to_birthday() != f"\033[31mtoday\033[0m"
        ):
            return (
                start_line
                + "\u2502 \033[34mContact name:\033[0m {: <{width1}}\u2502 \033[34mphones:\033[0m {}  \u2502 \033[34mbirthday:\033[0m {} (\033[34m{: <3}\033[0m days to birthday)\u2502  \033[34memail:\033[0m {: <{width2}}\u2502 \033[34maddress:\033[0m {: <{width3}}\u2502".format(
                    self.name.value,
                    f"{phone_fuller}".join(p.value for p in self.phones),
                    self.birthday.value,
                    self.days_to_birthday(),
                    self.email.value,
                    self.address.value,
                    width1 = longest['name'],
                    width2 = longest['email'],
                    width3 = longest['address']
                )
                + separation_line
            )
            

        elif self.birthday.value == "unknown":
            return (
                start_line
                + "\u2502 \033[34mContact name:\033[0m {: <{width1}}\u2502 \033[34mphones:\033[0m {}  \u2502 \033[34mbirthday:\033[0m {: <33}\u2502  \033[34memail:\033[0m {: <{width2}}\u2502 \033[34maddress:\033[0m {: <{width3}}\u2502".format(self.name.value,
                    f"{phone_fuller}".join(p.value for p in self.phones),
                    self.birthday.value,
                    self.email.value,
                    self.address.value,
                    width1 = longest['name'],
                    width2 = longest['email'],
                    width3 = longest['address']
                )
                + separation_line
            )

        elif self.days_to_birthday() == f"\033[31mtoday\033[0m":
            return (
                start_line
                + "\u2502 \033[34mContact name:\033[0m {: <{width1}}\u2502 \033[34mphones:\033[0m {}  \u2502 \033[34mbirthday:\033[0m {} {: ^31}\u2502  \033[34memail:\033[0m {: <{width2}}\u2502 \033[34maddress:\033[0m {: <{width3}}\u2502".format(
                    self.name.value,
                    f"{phone_fuller}".join(p.value for p in self.phones),
                    self.birthday.value,
                    self.days_to_birthday(),
                    self.email.value,
                    self.address.value,
                    width1 = longest['name'],
                    width2 = longest['email'],
                    width3 = longest['address']
                )
                + separation_line
            )
        

   

        

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self[str(record.name)] = record

    def find(self, name) -> Record:
        if name in self.keys():
            found_rec = self.get(name)
            return found_rec

    def delete(self, name):
        if name in self.keys():
            self.pop(name)

    def iterator(self, max_records=2) -> Iterator:
        indx = 0
        page = 1
        print_page = f"\n Page {page}\n"
        for rec in self.data.values():
            print_page += f"{rec}\n"
            indx += 1
            if indx >= max_records:
                yield print_page
                print_page = ""
                print_page = f"\n Page {page + 1}\n"
                indx = 0
                page += 1
        if indx > 0:
            yield print_page

    def load(self):
        file_name = "book.bin"
        try:
            load_dir = Path(__file__).resolve().parent
            file_path = load_dir.joinpath(file_name)
            with open(file_path, "rb") as fb:
                self.data = pickle.load(fb)
                print(
                    f"\033[32mAddressBook with {len(self.data)} contacts is succesfuly uploaded\033[0m"
                )
                return self.data
        except FileNotFoundError:
            book = AddressBook()

    def save(self):
        file_name = "book.bin"
        save_dir = Path(__file__).resolve().parent
        file_path = save_dir.joinpath(file_name)
        with open(file_path, "wb") as fb:
            pickle.dump(self.data, fb)
            print("\033[32mAddressBook is saved as book.bin\033[0m")
        return None