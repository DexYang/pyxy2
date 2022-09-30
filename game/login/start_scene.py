from core.scene import LoginScene
from data.login.start_scene import res
from settings import UI
from core.ui.button import Button
from core.ui.animation_node import AnimationNode
from core.ui.static_node import StaticNode


class StartScene(LoginScene):
    def __init__(self):
        super().__init__()

        self.scene_class_name = "StartScene"
        self.title = "游戏开始"

        for k, v in res[UI]["static"].items():
            static = StaticNode(name=k, **v)
            self.ui_layer.add_child(static)

        for k, v in res[UI]["animation"].items():
            ani = AnimationNode(name=k, **v)
            self.ui_layer.add_child(ani)

        buttons = res[UI]["buttons"]
        self.进入游戏 = Button(name="进入游戏", **buttons["进入游戏"])
        self.进入游戏.click = lambda : self.emit("change_scene", scene_name="NoteScene")
        self.ui_layer.add_child(self.进入游戏)

        self.注册账号 = Button(name="注册账号", **buttons["注册账号"])
        self.注册账号.click = lambda : print("注册账号")
        self.ui_layer.add_child(self.注册账号)

        self.退出游戏 = Button(name="退出游戏", **buttons["退出游戏"])
        self.退出游戏.click = lambda : self.emit("quit")
        self.ui_layer.add_child(self.退出游戏)

        self.play("gires2.wdf", "0xF7426640", True)  # 水流声
    
    def exit(self):
        self.sound.stop_loop_sound()
        super().exit()

