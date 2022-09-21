from core.ref import Ref
from core.role_manager import role_manager


class Scene(Ref):
    def __init__(self):
        super().__init__()

        self.scene_class_name = ""
        self.title = ""

        # self.ui_layer = AbstractUI()

        self.world_layer = None

    def handle_events(self, event):
        # self.ui_layer.handle_events(event)
        self.world_layer.handle_events(event)

    def update(self, context):
        # self.ui_layer.update(context)
        self.world_layer.update(context)

    def draw(self, _screen):
        self.world_layer.draw(_screen)
        # self.ui_layer.draw(_screen)

    def enter(self):
        role_manager.load_into(scene=self)
        self.world_layer.window_update(role_manager.main_role.x, role_manager.main_role.y, True)

    def exit(self):
        pass
