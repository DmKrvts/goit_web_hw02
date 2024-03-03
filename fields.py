from abc import ABC, abstractmethod
from datetime import datetime as dt, timedelta
import pickle
import random
import os


class Field(ABC):
    @abstractmethod
    def is_valid(self, value):
        pass


class Name(Field):
    def __init__(self, first_name: str, last_name: str = "", middle_name: str = ""):
        if self.is_valid(first_name):
            self.first_name = first_name
        else:
            print(f"Sorry, provided first name: '{first_name}' is not valid")
            patience = random.randint(5, 8)
            attempt = 0
            while attempt < patience:
                attempt += 1
                warning = input(
                    "Please note, the first name is mandatory, and should be at least one character long\nPlease provide First name:\n..>")
                if self.is_valid(warning):
                    self.first_name = warning
                    break

        self.last_name = last_name
        self.middle_name = middle_name

    def is_valid(self, value):
        if value.isalpha() and len(value) > 0:
            return True

    def __str__(self):
        if self.middle_name and self.last_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        elif self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return f"{self.first_name}"


class PhoneNumber(Field):
    def __init__(self, phone_number: str = ""):
        if self.is_valid(phone_number):
            self.phone_number = phone_number
        else:
            self.phone_number = ""
            self.phone_number_draft = phone_number

    def is_valid(self, value):
        if value.isdigit() and 10 <= len(value) <= 12:
            return True

    def __str__(self):
        return str(self.phone_number)


class Record:
    def __init__(self, name: Name, phone: PhoneNumber):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

    def __str__(self):
        return f"{self.name}: {self.phones[0]}"


class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def find_record(self, request):
        search_result = []
        for record in self.records:
            if request in record.name.first_name or request in record.name.last_name or request in record.name.middle_name:
                search_result.append(record)
        if search_result:
            for record in search_result:
                print(record)
            return search_result
        else:
            print(f"No matches found for the request:'{request}'")

    def log(self, action):
        current_time = dt.strftime(dt.now(), '%H:%M:%S')
        message = f'[{current_time}] {action}'
        with open('logs.txt', 'a') as file:
            file.write(f'{message}\n')

    def save(self, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump(self.records, file)
        self.log("Addressbook has been saved!")

    def load(self, file_name):
        emptyness = os.stat(file_name)
        if emptyness.st_size != 0:
            with open(file_name, 'rb') as file:
                self.records = pickle.load(file)
            self.log("Addressbook has been loaded!")
        else:
            with open(file_name, 'rb') as file:
                self.records = pickle.load(file)
            self.log('Adressbook has been created!')
        return self.records

    def __str__(self):
        if self.records:
            for record in self.records:
                print(record)
            return 'book'


class Bot:
    def __init__(self):
        self.book = AddressBook()

    def handle(self, action):
        if action == "add":
            first = (input("Please provide First name: \n..>"))
            last = (input("Please provide Last name(hit enter to skip): \n..>"))
            middle = (
                input("Please provide Middle name(hit enter to skip): \n..>"))
            try:
                name = Name(first, last, middle)
                phone = PhoneNumber(
                    input(f"Please provide phone number(only digits) for {name.first_name}(hit enter to skip): \n..>  +"))
                if phone.phone_number == "":
                    print(f"Please note, since provided phone number '{
                          phone.phone_number_draft}' is not valid, it was only saved as draft, you may edit it later")
                record = Record(name, phone)
                print(f"The record [{record}] was created and saved")
                return self.book.add_record(record)
            except Exception:
                print(
                    "Why even bother trying to create a record without the valid name, or even nickname?")
        elif action == "view":
            print(self.book)
        elif action == "search":
            request = input("Please provide search request: \n..>")
            self.book.find_record(request)


if __name__ == "__main__":
    print('Hello. I am your contact-assistant. What should I do with your contacts?')
    bot = Bot()
    bot.book.load("auto_save")
    commands = ['Add', 'Search', 'Edit', 'Load',
                'Remove', 'Save', 'Congratulate', 'View', 'Exit']
    while True:

        action = input(
            'Type help for list of commands or enter your command\n').strip().lower()
        if action == 'help':
            format_str = str('{:%s%d}' % ('^', 20))
            for command in commands:
                print(format_str.format(command))
            action = input().strip().lower()
            bot.handle(action)
            if action in ['add', 'remove', 'edit']:
                bot.book.save("auto_save")
        else:
            bot.handle(action)
            if action in ['add', 'remove', 'edit']:
                bot.book.save("auto_save")
        if action == 'exit':
            break


# test_bot = Bot()

# test_bot.handle("add")
# print(test_bot.book)


# one_phone = PhoneNumber("1122334455")
# print(one_phone)

# one_name = Name("Dm", "Krvts", "Andr")
# print(one_name)

# one_record = Record(one_name, one_phone)
# print(one_record)

# two_record = Record(Name("Kt", "Khn"), PhoneNumber("0099887766"))
# print(two_record)
# two_record.name.last_name = "khen"
# print(two_record)
# test_book = AddressBook()
# test_book.add_record(one_record)
# test_book.add_record(two_record)
# print("*" * 80)
# print(test_book)
