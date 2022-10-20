from core.director import Director
from lib.pyxy2 import MapThread
from core.animated.character import Character
from core.res_manager import res_manager

from game.login.start_scene import StartScene
from game.login.note_scene import NoteScene
from game.login.login_scene import GameLoginScene
from game.login.role_select import RoleSelect
from game.login.role_create import RoleCreate
from game.scenes.world_scene import WorldScene



if __name__ == '__main__':
    # res_manager.get("gires4.wdf", "经典红木/其他/血条栏/头像框.tcp")

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

    director.run("StartScene")
