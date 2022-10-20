import importlib

from core.scene import Scene
from core.world import World

from core.ui.static_node import StaticNode, ExtWidthStatic
from core.ui.input import Input

from .quic_buttons import get_quic_buttons

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
        keys = list(res[UI]["状态"].keys())
        x = WindowSize[0]
        for k in range(len(keys) - 1, -1, -1):
            v = res[UI]["状态"][keys[k]]
            static = StaticNode(name=keys[k], **v)
            static.x = x - static.w
            x -= static.w
            self.ui_layer.add_child(static)

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
        
       