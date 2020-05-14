from utility.utility import singleton
import sqlalchemy as db


@singleton
class DBConnection:
    __DB_PATH = 'postgresql+psycopg2://postgres:12345@localhost:8080/HCS'
    __engine = db.create_engine(__DB_PATH, encoding='UTF-8')
    __metadata = db.MetaData(__engine)

    @staticmethod
    def getConn():
        return DBConnection.__engine.connect()


if __name__ == '__main__':
    db = DBConnection()
    res = db.getConn().execute('select * from private.users;')
    print(res)
    print(tuple(res))
    pass

# import sqlalchemy as db
# from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Sequence,
# BigInteger, PrimaryKeyConstraint
# class ConnectionToDatabase:
#
#     __
#     @staticmethod
#     def getConnection():
# users = ''
# def createTable():
#     global users
#     users = Table('users_in', metadata,
#                   Column('id', Integer, primary_key=True, autoincrement=True),
#                   Column('fullname', String, nullable=False),
#                   Column('password', String, nullable=False),
#                   Column('age', Integer, nullable=False),
#                   Column('role', String, nullable=False),
#                   Column('gender', String, nullable=False),
#                   Column('phone', BigInteger, unique=True),
#                   Column('address', String),
#                   Column('image', String),
#                   schema='private'
#                   )
#     print(str(users.create()))
#
# def dropTable():
#     with engine.connect() as conn:
#         conn.execute('Drop Table private.user_in;')
#
#
#
# def ExecuteSelectSQL(uid, mode='show'):
#     select_statement = users.select().where(users.c.id == uid)
#     if mode == 'show':
#         print(str(select_statement))
#         print(select_statement.compile().params)
#     elif mode == 'execute':
#         with engine.connect() as conn:
#             result = conn.execute(select_statement)
#             return result
#
#
# def ExecuteUpdateSQL(uid, mode='show', **kwarg):
#     update_statement = users.update().where(users.c.id == uid).values(kwarg)
#     if mode == 'show':
#         print(str(update_statement))
#         print(update_statement.compile().params)
#     elif mode == 'execute':
#         with engine.connect() as conn:
#             conn.execute(update_statement)
#             return True
#
#
# def ExecuteInsertSQL(mode='show', fullname='', password='', age=30, role='', gender='',
#                      phone=None, address=None, image='../static/person.jpg'):
#     insert_statement = users.insert().values(fullname=fullname, password=password, age=age, role=role, gender=gender,
#                                              phone=phone, address=address, image=image)
#     if mode == 'show':
#         print(str(insert_statement))
#         print(insert_statement.compile().params)
#     elif mode == 'execute':
#         with engine.connect() as conn:
#             result = conn.execute(insert_statement)
#             return result
#
#
# def ExecuteDeleteSQL(uid, mode='show'):
#     delete_statement = users.delete().where(users.c.id == uid)
#
#     if mode == 'show':
#         print(str(delete_statement))
#         print(delete_statement.compile().params)
#     elif mode == 'execute':
#         with engine.connect() as conn:
#             conn.execute(delete_statement)
#             return True
