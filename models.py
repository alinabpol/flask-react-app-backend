from peewee import *
from flask_login import UserMixin


DATABASE = SqliteDatabase('dogs.sqlite')


class Dog(Model):
    name = CharField()
    age = IntegerField()
    breed = CharField()

    class Meta:
        database = DATABASE

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Dog, User], safe=True)
    print("TABLES Created")
    DATABASE.close()