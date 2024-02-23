from peewee import SqliteDatabase, Model, IntegrityError
from database.models import User, History, Custom


def create_user(id, name, first_n):
    created_user = False
    try:
        User.create(
            user_id=id,
            username=name,
            first_name=first_n
        )
        created_user = True
    except IntegrityError:
        created_user = False
    return created_user


def create_history(user_id, command, city_name=None):
    History.create(
        user=user_id,
        command=command,
        city=city_name
    )


def create_custom(user_id, t_min, t_max):
    Custom.create(
        user=user_id,
        temp_min=t_min,
        temp_max=t_max
    )
