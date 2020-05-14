from abc import ABC, abstractmethod


class User(ABC):
    """Not meant to instantiate objects"""

    def __init__(self, name):
        self.__name = name
        self.__id = None
        self.__gender = ''
        self.__address = ''
        self.__phone = ''
        self.__age = 0

    def __getID(self):
        return self.__id

    def __setID(self, id):
        self.__id = id

    id = property(__getID, __setID, )

    def __getName(self):
        return self.__name

    def __setName(self, name):
        self.__name = name

    name = property(__getName, __setName, )

    def __getAge(self):
        return self.__age

    def __setAge(self, age):
        self.__age = age

    age = property(__getAge, __setAge)

    def __getGender(self):
        return self.__gender

    def __setGender(self, gender):
        self.__gender = gender

    gender = property(__getGender, __setGender, )

    def __getAddress(self):
        return self.__address

    def __setAddress(self, address):
        self.__address = address

    address = property(__getAddress, __setAddress, )

    def __getPhone(self):
        return self.__phone

    def __setPhone(self, phone):
        self.__phone = phone

    phone = property(__getPhone, __setPhone, )

    def __str__(self):
        data = ''
        for attr, value in self.__dict__.items():
            if 'password' in attr:
                continue
            if 'User' in attr:
                data += attr[7:] + ': ' + str(value) + '\n'
            elif 'Patient' in attr:
                data += attr[10:] + ': ' + str(value) + '\n'
            elif 'Employee' in attr:
                data += attr[11:] + ': ' + str(value) + '\n'

        return data[:-1]

    @abstractmethod
    def update(self):
        pass


if __name__ == "__main__":
    # print(User('yazeed.', 'asd'))
    pass
