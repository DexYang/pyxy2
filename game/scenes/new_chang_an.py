from core.scene import Scene
from core.world import World


class NewChangAn(Scene):
    def __init__(self):
        super().__init__()

        self.scene_class_name = "NewChangAnScene"
        self.title = "长安城"

        self.world_layer = World('newscene', '1410')
