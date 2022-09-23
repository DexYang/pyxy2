from core.director import Director
from lib.pyxy2 import MapThread
from core.animated.character import Character
from core.role_manager import role_manager

from game.scenes.old_chang_an import OldChangAn
from game.scenes.new_chang_an import NewChangAn


if __name__ == '__main__':
    director = Director(title="大话西游II")

    director.init_scene({
        "OldChangAnScene": OldChangAn,
        "NewChangAnScene": NewChangAn
    })

    map_thread = MapThread()

    map_thread.start()

    role = Character(1, 500, 500)

    role_manager.main_role = role

    director.run("OldChangAnScene")
