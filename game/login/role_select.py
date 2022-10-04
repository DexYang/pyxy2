from core.scene import LoginScene
from data.login.role_select import res
from settings import UI
from core.ui.button import Button
from core.ui.animation_node import AnimationNode
from core.ui.static_node import StaticNode
from core.ui.one_pic_button import OnePicButton
from core.ui.text_button import TextButton


class RoleSelect(LoginScene):
    def __init__(self):
        super().__init__()
        
        self.scene_class_name = "RoleSelect"
        self.title = "角色选择"
        
        for k, v in res[UI]["static"].items():
            static = StaticNode(name=k, **v)
            self.ui_layer.add_child(static)
        
        buttons = res[UI]["buttons"]
        self.创建按钮 = Button(name="创建按钮", **buttons["创建按钮"])
        self.创建按钮.click = lambda : self.emit("tip", text="#24#Y创建功能还没写呢")
        self.ui_layer.add_child(self.创建按钮)

        self.取消按钮 = Button(name="取消按钮", **buttons["取消按钮"])
        self.取消按钮.click = lambda : self.emit("tip", text="#24#Y取消功能还没写呢")
        self.ui_layer.add_child(self.取消按钮)

        self.进入按钮 = Button(name="进入按钮", **buttons["进入按钮"])
        self.进入按钮.click = lambda : self.emit("change_scene", scene_name="OldChangAnScene")
        self.ui_layer.add_child(self.进入按钮)
