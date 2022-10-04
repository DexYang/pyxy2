from core.scene import LoginScene
from data.login.start_scene import res
from settings import UI
from core.ui.button import Button
from core.ui.animation_node import AnimationNode
from core.ui.static_node import StaticNode
from core.ui.one_pic_button import OnePicButton
from core.ui.text_button import TextButton


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
        self.注册账号.click = lambda : self.emit("tip", text="#24#Y注册功能还没写呢")
        self.ui_layer.add_child(self.注册账号)

        self.退出游戏 = Button(name="退出游戏", **buttons["退出游戏"])
        self.退出游戏.click = lambda : self.emit("exit")
        self.ui_layer.add_child(self.退出游戏)

        self.play(**res[UI]["sound"]["water_sound"])  # 水流声
        
        # self.pic_button = OnePicButton("photo.wdf", "facesmall/1.tga")
        # self.ui_layer.add_child(self.pic_button)
        # def pic_button_click():
        #     self.pic_button.selected = True
        # self.pic_button.click = pic_button_click
        
        # self.text_button = TextButton("测试按钮", x=100, y = 100, normal="")
        # self.ui_layer.add_child(self.text_button)
        # def text_button_click():
        #     self.pic_button.selected = False
        # self.text_button.click = text_button_click
    
    def exit(self):
        self.sound.stop_loop_sound(wdf=res[UI]["sound"]["water_sound"]["wdf"], was_hash=res[UI]["sound"]["water_sound"]["was_hash"])
        super().exit()

