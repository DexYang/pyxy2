from socket import gaierror
from core.director import Director
from lib.pyxy2 import MapThread
from core.animated.character import Character
from core.role_manager import role_manager
from core.res_manager import res_manager

from game.scenes.old_chang_an import OldChangAn
from game.scenes.new_chang_an import NewChangAn
from game.login.start_scene import StartScene
from game.login.note_scene import NoteScene
from game.login.login_scene import GameLoginScene

from core.ui.text import Text


if __name__ == '__main__':

    director = Director(title="大话西游II")

    director.init_scene({
        "StartScene": StartScene,
        "NoteScene": NoteScene,
        "LoginScene": GameLoginScene,
        "OldChangAnScene": OldChangAn,
        "NewChangAnScene": NewChangAn
    })

    map_thread = MapThread()

    map_thread.start()

    role = Character(1, 5100, 4200)

    role_manager.main_role = role

    director.run("StartScene")
