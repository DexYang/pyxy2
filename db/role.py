from db import db, Query

role_table = db.table('roles')
Roles = Query()


def get_roles(username):
    return role_table.search(Roles.username == username)


def exist_role_name(role_name):
    Roles = Query()
    return len(role_table.search(Roles.name == role_name)) > 0


def create_roles(username, role):
    role_table.insert({'username': username, **role})


def update_role(username, role):
    role_table.update(role, ((Roles.username == username) | (Roles.name == role["name"])))
