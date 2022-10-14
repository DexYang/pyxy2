from tkinter import E
from core.scene import Scene
from core.world import World
import importlib


class WorldScene(Scene):
    def __init__(self, map_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.world_layer = World(map_id)

        try:
            portals = importlib.import_module('game.scenes.'+str(map_id)).portal
            for p in portals:
                self.world_layer.add_child(p)
        except Exception as e:
            self.log.info(e)
