from models.users import User
from models.db import DBConnection as db
import functools as ft
import operator

from sqlalchemy.exc import IntegrityError


class Patient(User):
    def __init__(self, id):

        user_data = tuple(db().getConn().execute(
            f"select name, age, gender, phone, address from private.patiant "
            f"where id = {id};"))

        super().__init__(name=user_data[0][0])
        self.id = id
        self.age = user_data[0][1]
        self.gender = user_data[0][2]
        self.phone = user_data[0][3]
        self.address = user_data[0][4]

        user_data = list(db().getConn().execute(
            f"select allergie from private.allergies "
            f"where p_id = {id};"))

        self.__allergiesList = ft.reduce(operator.iconcat, user_data, [])

    def __getAllergiesList(self):
        return self.__allergiesList.copy()

    def modifyAllergiesList(self, allergiesList, mode='replace'):
        if not isinstance(allergiesList, list):
            raise TypeError("'allergiesList' must be of type list.")

        if mode == 'add':
            self.__allergiesList = self.__allergiesList + allergiesList
        elif mode == 'remove':
            self.__allergiesList = self.__allergiesList - allergiesList
        else:
            self.__allergiesList = allergiesList.copy()

    allergiesList = property(__getAllergiesList, )

    def update(self):
        db().getConn().execute(
            f"UPDATE private.patiant SET "
            f"id = {self.id}, "
            f"name = '{self.name}', "
            f"gender = '{self.gender}', "
            f"address = '{self.address}', "
            f"phone = '{self.phone}', "
            f"age = {self.age} "
            f"where id = {self.id} ")

        for item in self.__allergiesList:
            try:
                db().getConn().execute(
                    f"Insert into private.allergies (p_id, allergie) "
                    f"values ({self.id}, '{item}')")
            except IntegrityError:
                pass

        return True


if __name__ == "__main__":
    # x = Patient(15)
    # print(x)
    # print('-' * 100)
    # x.modifyAllergiesList(['Summer'], 'add')
    # print(x)
    # print('-' * 100)
    #
    # print(x.allergiesList)
    # print('-' * 100)
    # x.update()
    # print(x)
    # print('-' * 100)

    pass
