from core.scene import LoginScene
from data.login.role_create import res
from settings import UI
from core.ui.button import Button
from core.ui.animation_node import AnimationNode
from core.ui.static_node import StaticNode
from core.ui.one_pic_button import OnePicButton
from core.ui.text_button import TextButton
from data.character import characters

class RoleCreate(LoginScene):
    def __init__(self):
        super().__init__()
        
        self.scene_class_name = "RoleCreate"
        self.title = "角色创建"
        
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

        self.离开按钮 = Button(name="离开按钮", **buttons["离开按钮"])
        self.离开按钮.click = lambda : self.emit("tip", text="#24#Y离开功能还没写呢")
        self.ui_layer.add_child(self.离开按钮)

        self.selected = 0

        self.char_button = {}

        for k, v in res[UI]["char"].items():
            self.char_button[k] = OnePicButton(**v, name=k)
            def click(this):
                self.select(this.name)
                this.selected = True
            self.char_button[k].click = self.char_button[k].method(click)
            self.ui_layer.add_child(self.char_button[k])

        self.weapon_1 = None
        self.weapon_2 = None

        self.ui_layer.on_mouse_left_down = lambda event: print(event.pos)

    def select(self, char_id):
        for v in self.char_button.values(): 
            v.selected = False
        self.selected = char_id
        if self.weapon_1:
            self.weapon_1.destroy()
            self.weapon_2.destroy()
        weapon_id = list(characters[char_id]["武器"].values())
        weapon_name = list(characters[char_id]["武器"].keys())
        self.weapon_1 = AnimationNode("shape", "char/{:04d}/{}.tcp".format(weapon_id[0], "attack"), x=75, y=435, animation_rate=80)
        self.weapon_2 = AnimationNode("shape", "char/{:04d}/{}.tcp".format(weapon_id[1], "attack"), x=190, y=435, animation_rate=80)

    def update(self, context):
        self.ui_layer.update_children(context)
        if self.selected != 0:
            self.weapon_1.update(context)
            self.weapon_2.update(context)

    def draw(self, screen):
        self.ui_layer.draw_children(screen)
        if self.selected != 0:
            self.weapon_1.draw(screen)
            self.weapon_2.draw(screen)
        
