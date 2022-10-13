from core.director import Director
from lib.pyxy2 import MapThread
from core.animated.character import Character
from core.role_manager import role_manager
from core.scene import WorldScene

from game.scenes.old_chang_an import OldChangAn
from game.scenes.new_chang_an import NewChangAn
from game.login.start_scene import StartScene
from game.login.note_scene import NoteScene
from game.login.login_scene import GameLoginScene
from game.login.role_select import RoleSelect
from game.login.role_create import RoleCreate



if __name__ == '__main__':

    director = Director(title="大话西游II")

    director.init_scene({
        "StartScene": StartScene,
        "NoteScene": NoteScene,
        "LoginScene": GameLoginScene,
        "RoleSelect": RoleSelect,
        "RoleCreate": RoleCreate,
        "World": WorldScene
    })

    map_thread = MapThread()

    map_thread.start()

    role = Character(1, 5100, 4200)

    role_manager.main_role = role

    director.run("StartScene")
