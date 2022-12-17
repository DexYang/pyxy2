# from tinydb import TinyDB, Query
# import tinydb_encrypted_jsonstorage as tae
# KEY = "hello"
# PATH = "D:/.encrypted_db"
# # db = TinyDB(encryption_key=KEY, path=PATH, storage=tae.EncryptedJSONStorage)
# db = TinyDB(path="D:/test.json")


# from db.user import add_user, get_user, user_table

# # print(add_user("test"))
# user = get_user("username")
# print(user.doc_id)


# from slpp import slpp as lua
# code = """{

# }"""

# print(lua.decode(code))

# from distutils.core import setup
# from Cython.Build import cythonize

# setup(
#   name = 'Hello world app',
#   ext_modules = cythonize("settings.py"),
# )

# import aiohttp
# import asyncio

# async def main():

#     async with aiohttp.ClientSession() as session:
#         async with session.get('http://python.org') as response:

#             print("Status:", response.status)
#             print("Content-type:", response.headers['content-type'])

#             html = await response.text()
#             print("Body:", html[:15], "...")

# asyncio.run(main())


from core.flow import Flow, Conversation


model = Conversation()

print(model.state)    # solid
print(model.get())
model.proceed(0)
model.proceed()

print(model.state)    # solid
print(model.get())

model.proceed(0)
model.proceed()

print(model.state)    # solid
print(model.get())