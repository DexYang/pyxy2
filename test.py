# from tinydb import TinyDB, Query
# import tinydb_encrypted_jsonstorage as tae
# KEY = "hello"
# PATH = "D:/.encrypted_db"
# # db = TinyDB(encryption_key=KEY, path=PATH, storage=tae.EncryptedJSONStorage)
# db = TinyDB(path="D:/test.json")


from db.user import add_user, get_user, user_table

# print(add_user("test"))
user = get_user("username")
print(user.doc_id)


# from slpp import slpp as lua
# code = """{

# }"""

# print(lua.decode(code))