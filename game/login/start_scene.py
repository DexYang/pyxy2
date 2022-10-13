from audioop import add
from core.scene import LoginScene
from core.ui.label_button import LongLabelButton
from data.login.start_scene import res
from db import user
from settings import UI
from core.ui.button import Button
from core.ui.animation_node import AnimationNode
from core.ui.static_node import StaticNode
from core.ui.input import Input
from core.ui.dialog import ModalDialog
from core.ui.text import TextWrapper
from db.user import add_user


class StartScene(LoginScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        def register_click(): 
            self.register = Register('注册', 130, 170)
            self.ui_layer.add_child(self.register)
        self.注册账号.click = register_click
        self.ui_layer.add_child(self.注册账号)

        self.退出游戏 = Button(name="退出游戏", **buttons["退出游戏"])
        self.退出游戏.click = lambda : self.emit("exit")
        self.ui_layer.add_child(self.退出游戏)

        self.play(**res[UI]["sound"]["water_sound"])  # 水流声
    
    def exit(self):
        self.sound.stop_loop_sound(wdf=res[UI]["sound"]["water_sound"]["wdf"], was_hash=res[UI]["sound"]["water_sound"]["was_hash"])
        super().exit()

    def register(self):
        pass


class Register(ModalDialog): 
    def __init__(self, name, x=0, y=0):
        super().__init__('gires2.wdf', 'dialog/textinput.tcp', name=name, x=x, y=y)

        self.input = Input(x=42, y=71, w=350, h=16, no_chinese=True)
        self.add_child(self.input)

        self.注册 = TextWrapper("#Y注册", x=40, y=20)
        self.add_child(self.注册)

        self.确认 = LongLabelButton("确认", x=110, y=97)
        def confirm_click():
            username = self.input.get()
            if len(username) == 0: 
                self.emit("tip", text="#Y请输入用户名")
                return
            if add_user(username) > 0: 
                self.emit("tip", text="#Y账号注册成功 #1")
                self.useless = True
            else:
                self.emit("tip", text='#R该账号已存在 #24')
        self.确认.click = confirm_click
        self.add_child(self.确认)

        self.取消 = LongLabelButton("取消", x=230, y=97)
        def cancel_click():
            self.useless = True
        self.取消.click = cancel_click
        self.add_child(self.取消)

    def on_mouse_right_up(self, event): 
        if self.screen_rect.collidepoint(*event.pos):
            self.useless = True
        event.handled = True