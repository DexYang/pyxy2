from core.scene import LoginScene
from data.login.role_select import res
from settings import UI
from core.ui.button import Button
from core.ui.static_node import StaticNode
from core.ui.text import Text
from core.ui.text_button import TextButton
from core.role_manager import role_manager
from core.ui.scroll import Scroll
from data.character import 种族, 性别


class RoleSelect(LoginScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.scene_class_name = "RoleSelect"
        self.title = "角色选择"
        
        for k, v in res[UI]["static"].items():
            static = StaticNode(name=k, **v)
            self.ui_layer.add_child(static)
        
        buttons = res[UI]["buttons"]
        self.创建按钮 = Button(name="创建按钮", **buttons["创建按钮"])
        self.创建按钮.click = lambda : self.emit("change_scene", scene_name="RoleCreate")
        self.ui_layer.add_child(self.创建按钮)

        self.取消按钮 = Button(name="取消按钮", **buttons["取消按钮"])
        self.取消按钮.click = lambda : self.emit("change_scene", scene_name="LoginScene")
        self.ui_layer.add_child(self.取消按钮)

        self.进入按钮 = Button(name="进入按钮", **buttons["进入按钮"])
        self.进入按钮.click = lambda : self.enter_world()
        self.ui_layer.add_child(self.进入按钮)

        role_manager.get_roles()

        def click(this):
            self.select(this.value)

        self.role_list = Scroll(line_space=11, x=130, y=199, w=100, h=130)
        i = 0
        for role in role_manager.roles.values():
            button = TextButton(role["name"], normal="#W", value=role.doc_id)
            button.click = button.method(click)
            self.role_list.add_child(button)
            i += 1

        self.ui_layer.add_child(self.role_list)

        self.等级 = Text("", x=145, y=95, w=100, h=200)
        self.等级.hidden = True
        self.ui_layer.add_child(self.等级)

        self.性别 = Text("", x=145, y=122, w=100, h=200)
        self.性别.hidden = True
        self.ui_layer.add_child(self.性别)

        self.种族 = Text("", x=145, y=148, w=100, h=200)
        self.种族.hidden = True
        self.ui_layer.add_child(self.种族)

        self.头像 = None

        self.selected = 0

        if len(role_manager.roles) > 0:
            self.select(list(role_manager.roles.keys())[0])

    def select(self, value):
        photo_id = role_manager.roles[value]["photo"]
        self.selected = value
        if self.头像:
            self.头像.destroy()
        self.头像 = StaticNode("photo", "facelarge/{:d}.tga".format(photo_id), x=206, y=79)
        self.等级.set_text(role_manager.roles[value]["等级"])
        self.等级.hidden = False
        self.性别.set_text(性别[role_manager.roles[value]["性别"]])
        self.性别.hidden = False
        self.种族.set_text(种族[role_manager.roles[value]["种族"]])
        self.种族.hidden = False

    def update(self, context):
        self.ui_layer.update_children(context)
        if self.头像:
            self.头像.update(context)

    def draw(self, screen):
        self.ui_layer.draw_children(screen)
        if self.头像:
            self.头像.draw(screen)

    def enter_world(self):
        if self.selected == 0:
            self.emit("tip", text="#Y请先创建角色")
            return
        role_manager.select(self.selected)
        
