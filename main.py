from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        self.__value = ''.join(filter(str.isdigit, value))
        if len(value) == 10 or len(value) == 12:
            Field.value.fset(self, value)
        else:
            raise ValueError("Phone number must be 10 or 12 digits.")


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, "%Y-%m-%d").date()
            Field.value.fset(self, value)
        except ValueError:
            raise ValueError("Invalid birthdate format. Use YYYY-MM-DD.")


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = []
        if phone:
            self.phones.append(Phone(phone))
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        phone = Phone(phone)
        if phone not in self.phones:
            self.phones.append(phone)
            return f"Added phone number {phone} to {self.name}."
        return f"{phone} presents in phones of contact {self.name}"

    def remove_phone(self, phone):
        self.phones.remove(self.find_phone(phone))

    def change_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone == old_phone:
                phone = new_phone
                return f"Changed phone for {self.name} change to {new_phone}."
        return f"{old_phone}  not presents in phones of contact {self.name}"

    def find_phone(self, phone: Phone):
        for record in self.phones:
            if record == phone:
                return record
        return None

    def days_to_birthday(self, birthday):
        birthday_date = datetime.strptime(birthday, "%Y-%m-%d").date()
        current_date = datetime.now().date()
        if birthday_date:
            if birthday_date.year != current_date.year:
                birthday_date = birthday_date.replace(year=current_date.year)
            if current_date <= birthday_date:
                delta = birthday_date - current_date
                days = delta.days
            else:
                next_birthday_date = birthday_date.replace(
                    year=current_date.year + 1)
                delta = next_birthday_date - current_date
                days = delta.days
            return f"{days} days before the birthday"
        else:
            return None

    def __str__(self):
        birthday_str = f", birthday {self.birthday.value} " if self.birthday and self.birthday.value else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}{birthday_str}"


class AddressBook(UserDict):
    def __init__(self, records=None):
        super().__init__()
        if records:
            for record in records:
                self.add_record(record)

    def add_record(self, record: Record):
        if record.name.value in self.data:
            raise ValueError(
                f"Contact with the name {record.name.value} already exists.")
        self.data[record.name.value] = record
        return f"Contact {record} add success"

    def find(self, name):
        result = self.data.get(name)
        return result

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Deleted record for {name}."
        else:
            return f"No such record for {name}."

    def __str__(self) -> str:
        return "\n".join(str(record) for record in self.data.values())

    def __iter__(self):
        return self.record_iterator()

    def record_iterator(self, page_size=5):
        keys = list(self.data.keys())
        current_index = 0
        while current_index < len(keys):
            yield {key: self.data[key] for key in keys[current_index: current_index + page_size]}
            current_index += page_size
