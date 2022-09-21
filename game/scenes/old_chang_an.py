from core.scene import Scene
from core.world import World


class OldChangAn(Scene):
    def __init__(self):
        super().__init__()

        self.scene_class_name = "OldChangAnScene"
        self.title = "长安城"

        self.world_layer = World('scene', '1001')
