import importlib

from core.scene import Scene
from core.world import World

from core.ui.static_node import StaticNode, ExtWidthStatic
from core.ui.input import Input

from .quic_buttons import get_quic_buttons
from .state import 气血条, 法力条, 经验条

from data.world.ui import res 
from settings import UI, WindowSize

class WorldScene(Scene):
    def __init__(self, map_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # world_layer
        self.world_layer = World(map_id)

        try:
            portals = importlib.import_module('game.scenes.'+str(map_id)).portal
            for p in portals:
                self.world_layer.add_child(p)
        except Exception as e:
            self.log.info(e)
            
        # ui_layer
        #坐标
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
        self.召唤兽经验条 = 经验条(**res[UI]["state"]["兽经验"], x=x+42, y=4)
        self.ui_layer.add_child(self.召唤兽经验条)
        self.召唤兽气血条 = 气血条(**res[UI]["state"]["兽血"], x=x+42, y=15)
        self.ui_layer.add_child(self.召唤兽气血条)
        self.召唤兽法力条 = 法力条(**res[UI]["state"]["兽法"], x=x+42, y=26)
        self.ui_layer.add_child(self.召唤兽法力条)

        #快捷按钮
        buttons, w = get_quic_buttons()
        for button in buttons:
            self.ui_layer.add_child(button)

        # 聊天
        charframe = ExtWidthStatic(name=k, **res[UI]["聊天"]["聊天框"], w=w)
        charframe.y = WindowSize[1] - charframe.h
        self.ui_layer.add_child(charframe)

        self.input = Input(x=3, y=charframe.y+1, w=w, font_size=16, h=charframe.h)
        self.ui_layer.add_child(self.input)
        
       