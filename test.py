# from tinydb import TinyDB, Query
# import tinydb_encrypted_jsonstorage as tae
# KEY = "hello"
# PATH = "D:/.encrypted_db"
# db = TinyDB(encryption_key=KEY, path=PATH, storage=tae.EncryptedJSONStorage)


# Fruit = Query()
# db.update({'count': 10000}, Fruit.type == 'apple')

# db.remove(Fruit.count > 5)
# print(db.all())

# from lib import pyfmodex
# from lib.pyfmodex.flags import MODE
# from lib.pyfmodex.structures import CREATESOUNDEXINFO
# from core.res_manager import res_manager



# system = pyfmodex.System()

# system.init()

# item = res_manager.get("sound.wdf", "0x4F8F2281")



# sound = system.create_sound(item.data,
#                             mode=MODE.OPENMEMORY | MODE.LOOP_OFF,
#                             exinfo=CREATESOUNDEXINFO(length=item.size))

# channel = sound.play()

# import time

# time.sleep(1)

# channel = sound.play()

# time.sleep(100)
import pygame_textinput
import pygame
pygame.init()

# Create TextInput-object
textinput = pygame_textinput.TextInputVisualizer()

screen = pygame.display.set_mode((1000, 200))
clock = pygame.time.Clock()

while True:
    screen.fill((225, 225, 225))

    events = pygame.event.get()

    # Feed it with events every frame
    textinput.update(events)
    # Blit its surface onto the screen
    screen.blit(textinput.surface, (10, 10))

    for event in events:
        if event.type == pygame.QUIT:
            exit()

    pygame.display.update()
    clock.tick(30)