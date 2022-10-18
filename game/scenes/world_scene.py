import importlib
from operator import imod

from data.world.ui import res 
from core.scene import Scene
from core.world import World
from settings import UI

from core.ui.static_node import StaticNode

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
        for k, v in res[UI]["static"].items():
            static = StaticNode(name=k, **v)
            self.ui_layer.add_child(static)
       