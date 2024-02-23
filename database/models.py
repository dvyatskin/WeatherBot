import os
from peewee import Model, CharField, IntegerField, SqliteDatabase, AutoField, ForeignKeyField

db_user = SqliteDatabase(os.path.abspath(os.path.join('database', 'my_database.db')))
db_history = SqliteDatabase(os.path.abspath(os.path.join('database', 'history_database.db')))
db_custom = SqliteDatabase(os.path.abspath(os.path.join('database', 'custom_database.db')))


class User(Model):
    user_id = IntegerField(primary_key=True)
    username = CharField()
    first_name = CharField()

    class Meta:
        database = db_user


class History(Model):
    history_id = AutoField()
    user = ForeignKeyField(User, backref='histories')
    command = CharField()
    city = CharField()

    class Meta:
        database = db_history


class Custom(Model):
    custom_id = AutoField()
    user = ForeignKeyField(User, backref='customs')
    temp_min = IntegerField()
    temp_max = IntegerField()

    class Meta:
        database = db_custom


def create_models():
    db_user.create_tables([User, History, Custom])
