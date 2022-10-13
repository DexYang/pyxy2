from db import db, Query

user_table = db.table('users')


def add_user(username: str) -> int:
    if get_user(username):
        return 0
    return user_table.insert({'username': username, 'login': False})


def get_user(username: str) -> list:
    User = Query()
    return user_table.get(User.username == username)

