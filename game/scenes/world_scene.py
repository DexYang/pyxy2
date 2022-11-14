import os
import pkgutil

from core.scene import Scene
from core.world import World

from core.ui.node import Blank
from core.ui.static_node import StaticNode, ExtWidthStatic
from core.ui.input import Input
from core.role_manager import role_manager
from core.ui.one_pic_button import OnePicButton

from game.scenes.portal import Portal
from game.scenes.window_layer import WindowLayer

from .quic_buttons import get_quic_buttons
from .status import 气血条, 法力条, 经验条, 召唤兽气血条, 召唤兽法力条, 召唤兽经验条

from data.world.ui import res
from settings import UI, WindowSize


class WorldScene(Scene):
    def __init__(self, map_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.map_id = map_id

        # world_layer
        self.world_layer = World(map_id)

        # 加载地图目录下的类或对象，Portals
        self.load()
        # 加载地图目录下的NPC
        self.load('npc')

        self.win_layer = WindowLayer()

        self.ui_layer = Blank()
        # 坐标
        for k, v in res[UI]["坐标"].items():
            self.ui_layer.add_child(StaticNode(name=k, **v))

        # 状态
        x = WindowSize[0]
        static = StaticNode(name="人面板", **res[UI]["状态"]["人面板"])
        static.x = x - static.w
        x -= static.w
        self.ui_layer.add_child(static)
        self.经验条 = 经验条(**res[UI]["state"]["人经验"], x=x, y=5)
        self.ui_layer.add_child(self.经验条)
        self.气血条 = 气血条(**res[UI]["state"]["人血"], x=x, y=20)
        self.ui_layer.add_child(self.气血条)
        self.法力条 = 法力条(**res[UI]["state"]["人法"], x=x, y=35)
        self.ui_layer.add_child(self.法力条)

        static = StaticNode(name="头像框", **res[UI]["状态"]["头像框"])
        static.x = x - static.w
        x -= static.w
        self.ui_layer.add_child(static)

        static = StaticNode(name="兽面板", **res[UI]["状态"]["兽面板"])
        static.x = x - static.w
        x -= static.w
        self.ui_layer.add_child(static)
        self.召唤兽经验条 = 召唤兽经验条(**res[UI]["state"]["兽经验"], x=x + 42, y=4)
        self.ui_layer.add_child(self.召唤兽经验条)
        self.召唤兽气血条 = 召唤兽气血条(**res[UI]["state"]["兽血"], x=x + 42, y=15)
        self.ui_layer.add_child(self.召唤兽气血条)
        self.召唤兽法力条 = 召唤兽法力条(**res[UI]["state"]["兽法"], x=x + 42, y=26)
        self.ui_layer.add_child(self.召唤兽法力条)

        # 快捷按钮
        buttons, w = get_quic_buttons()
        for button in buttons:
            self.ui_layer.add_child(button)

        # 聊天
        chat_frame = ExtWidthStatic(name="聊天框", **res[UI]["聊天"]["聊天框"], w=w)
        chat_frame.y = WindowSize[1] - chat_frame.h
        self.ui_layer.add_child(chat_frame)

        self.input = Input(x=3, y=chat_frame.y + 2, w=w, font_size=16, h=chat_frame.h - 2)
        self.ui_layer.add_child(self.input)

        # 切换角色
        _y = 100
        for role_id, v in role_manager.roles.items():
            头像底 = StaticNode(y=_y, **res[UI]["头像底框"], w=31, h=31)
            self.ui_layer.add_child(头像底)
            头像 = OnePicButton(wdf="photo", was_hash="facesmall/{}.tga".format(str(v["photo"])), name=role_id,
                                x=1, y=_y + 2, value=role_id, w=27, h=27)

            def click(this):
                role_manager.main_role = this.value

            头像.click = 头像.method(click)
            self.ui_layer.add_child(头像)
            _y += 31

    def load(self, path = ""):
        path_list = [os.path.dirname(__file__) + "\\" + self.map_id + "\\" + path]
        for file_finder, name, _ in pkgutil.iter_modules(path_list):
            module = file_finder.find_module(name).load_module(name)
            try:
                for attr_name in module.__dir__():
                    if attr_name.startswith("__") or \
                        attr_name == "Portal" or \
                        attr_name == "NPC":
                        continue
                    attr = getattr(module, attr_name)
                    if type(attr) == type:
                        attr = attr()
                    self.world_layer.add_child(attr)
            except Exception as e:
                self.log.error(e)

