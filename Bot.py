from datetime import datetime
from collections import UserDict
import pickle

class AddressBook(UserDict):
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def remove_record(self, record):
        self.records.remove(record)

    def __iter__(self):
        yield from self.records
    
    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self.records, f)
    
    def load(self, filename):
        with open(filename, 'rb') as f:
            self.records == pickle.load(f)
    
class Record:
    def __init__(self, name, phones, birthday=None):
        self.name = name
        self.phones = phones
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

    def days_to_birthday(self):
        if self.birthday is None:
            return None
        today = datetime.today().date()
        birthday_this_year = self.birthday.replace(year=today.year)
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)
        days_to_birthday = (birthday_this_year - today).days
        return days_to_birthday
    

    def __str__(self):
        name_str = f"{self.name}: " if self.name else ""
        phones_str = ", ".join(self.phones)
        return f"{phones_str}" if self.name else phones_str



class Field:
    def __init__(self, value):
        self.set_value(value)

    def set_value(self, new_value):
        self.validate(new_value)
        self.value = new_value

    def validate(self, value):
        pass

class Name(Field):
    pass

class Phone(Field):
    def validate(self, value):
        if not value.isdigit():
            raise ValueError("Invalid phone number")

class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid birthday")

def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found"
        except ValueError:
            return "Invalid command format"
        except IndexError:
            return "Invalid command format"
    return wrapper

@input_error
def add(command, address_book):
    args = command.split()[1:]
    name = args[0]
    phones = args[1:]
    record = Record(name, phones)
    address_book.add_record(record)
    return f"{name} added with phone number: {', '.join(phones)}" if phones else f"{name} added without a phone number"

@input_error
def change(command, address_book):
    args = command.split()[1:]
    name = args[0]
    field_index = int(args[1])
    new_value = args[2]
    record = next(filter(lambda x: x.name == name, address_book))
    if field_index == 0:
        record.name = Name(new_value)
    elif field_index - 1 < len(record.phones):
        record.phones[field_index - 1].set_value(new_value)
    elif field_index == len(record.phones) + 1:
        record.birthday.set_value(new_value)
    else:
        raise ValueError("Invalid field index")
    return f"{name}'s field {field_index} updated to {new_value}"

@input_error
def show_all(address_book):
    if not address_book.records:
        return "No contacts found"
    return "\n".join([f"{record.name}: {record}" for record in address_book])


@input_error
def remove(command, address_book):
    name = command.split()[1]
    try:
        record = next(filter(lambda x: x.name == name, address_book))
    except StopIteration:
        return "Contact not found"
    address_book.remove_record(record)
    return f"{name} removed"

@input_error
def search(command, address_book):
    query = command.split()[1]
    results = []
    for record in address_book:
        if query in record.name:
            results.append(record)
        elif query in "".join(record.phones):
            results.append(record)
        elif record.birthday and query in record.birthday.value:
            results.append(record)
    if not results:
        return f"No contacts found containing {query}"
    return "\n".join([f"{record.name}: {record}" for record in results])

def main():
    address_book = AddressBook()
    print("How can I help you?")
    while True:
        command = input(">>>")
        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add "):
            print(add(command, address_book))
        elif command.startswith("change "):
            print(change(command, address_book))
        elif command.startswith("remove"):
            print(remove(command, address_book))
        elif command == "show all":
            print(show_all(address_book))
        elif command.startswith("save"):
            filename = command.split()[1]
            address_book.save(filename)
            print(f"Address book saved to {filename}")
        elif command.startswith("load"):
            filename = command.split()[1]
            address_book.load(filename)
            print(f"Address book loaded from {filename}")
        elif command.startswith("search"):
            print(search(command, address_book))
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command")


if __name__ == "__main__":
    main()
