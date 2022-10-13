from core.scene import LoginScene
from data.login.login_scene import res
from settings import UI
from core.ui.button import Button
from core.ui.static_node import StaticNode
from core.ui.input import Input
from db.user import get_user
from core.role_manager import role_manager


class GameLoginScene(LoginScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scene_class_name = "LoginScene"
        self.title = "游戏登录"

        for k, v in res[UI]["static"].items():
            static = StaticNode(name=k, **v)
            self.ui_layer.add_child(static)

        buttons = res[UI]["buttons"]
        self.登录 = Button(name="登录", **buttons["登录"])
        self.登录.click = lambda : self.login()
        self.ui_layer.add_child(self.登录)

        self.取消 = Button(name="取消", **buttons["取消"])
        self.取消.click = lambda : self.emit("change_scene", scene_name="NoteScene")
        self.ui_layer.add_child(self.取消)

        self.离开 = Button(name="离开", **buttons["离开"])
        self.离开.click = lambda : self.emit("change_scene", scene_name="StartScene")
        self.ui_layer.add_child(self.离开)

        self.username = Input(font_size=16, no_chinese=True, x=271, y=187, w=250, h=16)
        self.ui_layer.add_child(self.username)

    def on_text_enter(self, event):
        if event.input_id == self.username.id: 
            self.login()

    def login(self): 
        username = self.username.get()
        if not username: 
            self.emit("tip", text="#Y请输入用户名")
            return
        user = get_user(username)
        if not user: 
            self.emit("tip", text="#Y用户不存在: "+ username)
        else: 
            self.emit("tip", text="#Y欢迎回来 #38"+ username)
            role_manager.login(username)
            self.emit("change_scene", scene_name="RoleSelect")