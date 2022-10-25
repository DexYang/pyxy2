from core.scene import LoginScene
from data.login.role_create import res
from settings import UI
from core.ui.button import Button
from core.ui.animation_node import AnimationNode
from core.ui.static_node import StaticNode, StaticText
from core.ui.one_pic_button import OnePicButton
from data.character import characters, 种族, 性别
from core.ui.text import Text
from core.ui.input import Input
from core.role_manager import role_manager

from db.role import exist_role_name
from data.json.角色 import get角色


class RoleCreate(LoginScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scene_class_name = "RoleCreate"
        self.title = "角色创建"

        for k, v in res[UI]["static"].items():
            static = StaticNode(name=k, **v)
            self.ui_layer.add_child(static)

        buttons = res[UI]["buttons"]
        self.创建按钮 = Button(name="创建按钮", **buttons["创建按钮"])
        self.创建按钮.click = lambda: self.create()
        self.ui_layer.add_child(self.创建按钮)

        self.取消按钮 = Button(name="取消按钮", **buttons["取消按钮"])
        self.取消按钮.click = lambda: self.emit("change_scene", scene_name="RoleSelect")
        self.ui_layer.add_child(self.取消按钮)

        self.离开按钮 = Button(name="离开按钮", **buttons["离开按钮"])
        self.离开按钮.click = lambda: self.emit("change_scene", scene_name="StartScene")
        self.ui_layer.add_child(self.离开按钮)

        self.selected = 0

        self.char_button = {}

        def click(this):
            self.select(this.name, this.x, this.y)

        for k, v in res[UI]["char"].items():
            self.char_button[k] = OnePicButton(**v, name=k)
            self.char_button[k].click = self.char_button[k].method(click)
            self.ui_layer.add_child(self.char_button[k])

        self.weapon_1 = None
        self.weapon_2 = None

        self.desc = Text("", x=245, y=335, w=260, h=100, z=100, font_size=12)
        self.desc.hidden = True
        self.ui_layer.add_child(self.desc)

        self.武器1 = StaticText('gires3.wdf', '0xC9B82205', x=102, y=335, z=100)
        self.武器1_text = Text('武器1', x=4, y=2, w=16, h=50, font_size=12, line_space=1)
        self.武器1.add_child(self.武器1_text)
        self.武器1.hidden = True
        self.ui_layer.add_child(self.武器1)

        self.武器2 = StaticText('gires3.wdf', '0xC9B82205', x=212, y=335, z=100)
        self.武器2_text = Text('武器2', x=4, y=2, w=16, h=50, font_size=12, line_space=1)
        self.武器2.add_child(self.武器2_text)
        self.武器2.hidden = True
        self.ui_layer.add_child(self.武器2)

        self.选中 = StaticNode('gires2', 'login/selectrole.tca', "选中", z=100)
        self.选中.hidden = True
        self.ui_layer.add_child(self.选中)

        self.input = Input(x=344, y=437, w=113)
        self.ui_layer.add_child(self.input)

        self.ui_layer.on_mouse_left_down = lambda event: print(event.pos)

    def select(self, char_id, char_x, char_y):
        self.selected = char_id
        self.选中.x = char_x
        self.选中.y = char_y
        self.选中.hidden = False
        if self.weapon_1:
            self.weapon_1.destroy()
            self.weapon_2.destroy()
        weapon_id = list(characters[char_id]["武器"].values())
        weapon_name = list(characters[char_id]["武器"].keys())
        self.weapon_1 = AnimationNode("shape", "char/{:04d}/{}.tcp".format(weapon_id[0], "attack"), x=75, y=435,
                                      animation_rate=80)
        self.weapon_2 = AnimationNode("shape", "char/{:04d}/{}.tcp".format(weapon_id[1], "attack"), x=190, y=435,
                                      animation_rate=80)

        self.武器1_text.set_text("#R" + weapon_name[0])
        self.武器1_text.y = 8 if len(weapon_name[0]) == 1 else 2
        self.武器1.hidden = False

        self.武器2_text.set_text("#R" + weapon_name[1])
        self.武器2_text.y = 8 if len(weapon_name[1]) == 1 else 2
        self.武器2.hidden = False

        描述 = "#Y" + characters[char_id]["角色名"] + "#n#r" + characters[char_id]["描述"] + "#r【种族】" + \
            种族[characters[char_id]["种族"]] + \
            "   【性别】" + 性别[characters[char_id]["性别"]] + \
            "#r【门派】" + "、".join(characters[char_id]["门派"])
        self.desc.set_text(描述)
        self.desc.hidden = False

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

    def create(self):
        role_name = self.input.get()
        if len(role_name) == 0:
            self.emit("tip", text="请输入角色名称")
            return
        if exist_role_name(role_name):
            self.emit("tip", text="角色名称已存在")
            return
        role = get角色(self.selected, role_name)
        
        role_manager.create_role(role)
        self.emit("change_scene", scene_name="RoleSelect")
