from models.users import User
from models.db import DBConnection as db


class Employee(User):
    def __init__(self, email, name, password, role=0, image='../static/img/person.jpg'):
        super().__init__(name=name)
        self.__email = email
        self.__password = password
        self.__role = role
        self.__image = image

        user_data = tuple(db().getConn().execute(
            f"select gender, age, phone, address, id from private.users "
            f"where email = '{email}' and role = {self.role};"))

        self.gender = user_data[0][0]
        self.age = user_data[0][1]
        self.phone = user_data[0][2]
        self.address = user_data[0][3]
        self.id = user_data[0][4]

    def __getEmail(self):
        return self.__email

    def __setEmail(self, email):
        self.__email = email

    email = property(__getEmail, __setEmail)

    def __getPassword(self):
        return self.__password

    def __setPassword(self, password):
        self.__password = password

    password = property(__getPassword, __setPassword, )

    def __getImage(self):
        return self.__image
        pass

    def __setImage(self, image):
        self.__image = image
        pass

    image = property(__getImage, __setImage, )

    def __getRole(self):
        return self.__role
        pass

    def __setRole(self, role):
        self.__role = role
        pass

    role = property(__getRole, __setRole)

    def update(self):
        db().getConn().execute(
            f"UPDATE private.users SET "
            f"email = '{self.email}', "
            f"id = {self.id}, "
            f"name = '{self.name}', "
            f"gender = '{self.gender}', "
            f"address = '{self.address}', "
            f"phone = '{self.phone}', "
            f"age = {self.age}, "
            f"password = '{self.password}', "
            f"role = {self.role}, "
            f"image = '{self.image}' "
            f"where email = '{self.email}' "
            f"and role = {self.role};")
        return True


if __name__ == "__main__":
    x = Employee('yazeed.hasan.97@gmail.com', 'Yazeed Hasan', '123')
    print(x)
    x.password = '123'
    # x.update()
    print('-' * 100)
    print(x)
    pass
