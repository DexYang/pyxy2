from db import db, Query

user_table = db.table('users')
User = Query()

def add_user(username: str) -> int:
    if get_user(username):
        return 0
    return user_table.insert({'username': username, 'login': False})


def get_user(username: str) -> list:
    return user_table.get(User.username == username)


def login(username: str):
    return user_table.update({"login": True}, User.username == username)


def logout(username: str):
    return user_table.update({"login": False}, User.username == username)
