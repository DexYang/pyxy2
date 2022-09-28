from core.scene import Scene
from core.world import World

from core.ui.button import Button


class OldChangAn(Scene):
    def __init__(self):
        super().__init__()

        self.scene_class_name = "OldChangAnScene"
        self.title = "长安城"

        self.world_layer = World('scene', '1001')

        self.ui_layer.add_child(Button('gires2.wdf', 'login/btn_login.tcp', 'login'))


        
