from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other): # Перевірка на відповідність
        if isinstance(other, Field):
            return self.value == other.value
        return False

class Name(Field):
    def __init__(self, name):
        super().__init__(name)

class Phone(Field):
    def __init__(self, phone):
        self._value = None
        self.value = phone  

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, phone):
        if not re.fullmatch(r'\d{10}', phone):
            raise ValueError("Телефон має бути з 10 цифр.")
        self._value = phone

class Record:
    def __init__(self, name, phone=None):
        self.name = Name(name) if isinstance(name, str) else name
        self.phones = []
        if phone:
            self.add_phone(phone) # Заисали новий номер

    def add_phone(self, phone):
        phone_obj = Phone(phone) if isinstance(phone, str) else phone
        self.phones.append(phone_obj) # Добавка номера

    def remove_phone(self, phone):
        phone_value = phone if isinstance(phone, str) else phone.value # Видалення номера
        self.phones = [p for p in self.phones if p.value != phone_value]

    def edit_phone(self, old_phone, new_phone): # коризування номера
        old_value = old_phone if isinstance(old_phone, str) else old_phone.value
        new_obj = Phone(new_phone) if isinstance(new_phone, str) else new_phone
        for idx, p in enumerate(self.phones):
            if p.value == old_value:
                self.phones[idx] = new_obj
                return True
        return False

    def find_phone(self, phone_value): # Пошук номера
        for p in self.phones:
            if p.value == phone_value:
                return p
        return None

    def __str__(self):
        return f"Ім'я контакту: {self.name.value}, телефон: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args

def input_error(func): # Переверка на помилки
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Value error: {e}"
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Not enough arguments."
        except TypeError:
            return "Invalid input format."
    return inner


@input_error
def add_contact(args, contacts: AddressBook):
    name, phone = args
    record = contacts.find(name)
    if record:
        record.add_phone(phone)  # автоматично створює Phone
    else:
        record = Record(name, phone)
        contacts.add_record(record)
    return f"Контакт '{name}' створений/оновлений."


@input_error
def change_contact(args, contacts: AddressBook):
    name, old_phone, new_phone = args
    record = contacts.find(name)
    if not record:
        raise KeyError
    success = record.edit_phone(old_phone, new_phone)
    if success:
        return "Телефонний номер оновлений"
    return "Старий номер телефону не знайдений."


@input_error
def show_phone(args, contacts: AddressBook):
    name = args[0]
    record = contacts.find(name)
    if record:
        return str(record)
    raise KeyError

@input_error
def delete_contact(args, contacts: AddressBook):
    name = args[0]
    success = contacts.delete(name)
    if success:
        return f"Контакт '{name}' видалений."
    else:
        return f"Контакт '{name}' не знайдено."

@input_error
def find_contact_by_name(args, contacts: AddressBook):
    name = args[0]
    record = contacts.find(name)
    if record:
        return f"Знайдено: {record}"
    else:
        return f"Контакт з іменем '{name}' не знайдено."

def all_phone(contacts: AddressBook):
    if not contacts.data:
        return "Контакти не знайдено"
    return str(contacts)

def main():
    contacts = AddressBook()
    print("Привіт, вітаю вас в боті асистенті")

    while True:
        user_input = input("Введіть команду: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Бувай друже!")
            break
        elif command in ["hello", "hi"]:
            print("Чим можу допомогти?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(all_phone(contacts))
        elif command in ["delete", "del"]:
            print(delete_contact(args, contacts))
        elif command == "find":
            print(find_contact_by_name(args, contacts))
        elif command == "help":
            print("Доступні команди:\n"
                "add <name> <phone>\n"
                "change <name> <old_phone> <new_phone>\n"
                "delete / del <name>\n"
                "phone <name>\n"
                "find <name>\n"
                "all\n"
                "exit / close")
        else:
            print("Невідома команда. Введіть 'help' щоб переглянути список доступних команд.")


if __name__ == "__main__":
    main()

# Створення нової адресної книги
#    book = AddressBook()

#    # Створення запису для John
#   john_record = Record("John")
#   john_record.add_phone("1234567890")
#   john_record.add_phone("5555555555")

#    # Додавання запису John до адресної книги
#    book.add_record(john_record)
#
#    # Створення та додавання нового запису для Jane
#    jane_record = Record("Jane")
#    jane_record.add_phone("9876543210")
#    book.add_record(jane_record)
#
#    # Виведення всіх записів у книзі
#    for name, record in book.data.items():
#        print(record)

#    # Знаходження та редагування телефону для John
#    john = book.find("John")
#    john.edit_phone("1234567890", "1112223333")

#    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

#    # Пошук конкретного телефону у записі John
#    found_phone = john.find_phone("5555555555")
#    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

#    # Видалення запису Jane
#    book.delete("Jane")

#    # Виведення всіх записів у книзі
#    for name, record in book.data.items():
#        print(record)

