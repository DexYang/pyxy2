import os
import pkgutil
import importlib

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
from utils.is_chinese import is_chinese

base_path = 'game.scenes'


class MapConvert:
    _instance = None
    MAP_ID = {}

    def __new__(cls):
        if not hasattr(cls, '_instance') or cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        path = os.path.dirname(__file__)
        self.load(path)

    def load(self, path, prefix=""):
        for item in os.listdir(path):
            if os.path.isdir(os.path.join(path, item)) and is_chinese(item[0]):
                self.MAP_ID[prefix + item] = True
                self.load(path + "\\" + item, item + ".")


map_converter = MapConvert()


class WorldScene(Scene):
    def __init__(self, map_name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.map_name = map_name

        mod = importlib.import_module(base_path + '.' + self.map_name)
        self.map_id = mod.map_id
        
        self.world_layer = World(self.map_id)
        # 加载地图目录下的类或对象，Portals
        self.load()
        # 加载地图目录下的NPC
        self.load('npc')
        
        # world_layer
        

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

    def load(self, path=""):
        try:
            if path == "":
                mod = importlib.import_module(base_path + '.' + self.map_name)
                for portal in mod.portals:
                    self.world_layer.add_child(portal)
                self.map_id = mod.map_id
            else:
                abs_path = os.path.dirname(__file__) + "\\" + self.map_name.replace(".", "\\") + "\\" + path
                for item in os.listdir(abs_path):
                    if os.path.isfile(os.path.join(abs_path, item)) and is_chinese(item[0]):
                        name = base_path + '.' + self.map_name + '.' + path + '.' + item[:-3]
                        importlib.import_module(name)
                        module = importlib.find_loader(name).load_module(name)
                        for attr_name in module.__dir__():
                            if attr_name.startswith("_") or \
                                    attr_name == "Conversation" or \
                                    attr_name == "Portal" or \
                                    attr_name == "WorldNPC":
                                continue
                            attr = getattr(module, attr_name)
                            if type(attr) == type:
                                attr = attr()
                            self.world_layer.add_child(attr)
        except Exception as e:
            import traceback
            self.log.error(e)
            traceback.print_exc()

