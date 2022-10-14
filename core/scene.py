from core.ref import Ref
from core.role_manager import role_manager
from core.ui.node import Root
from settings import WindowSize
from core.world import World


class Scene(Ref):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.scene_class_name = ""
        self.title = ""

        self.win_layer = Root()

        self.ui_layer = Root()

        self.world_layer = None

        self.emit("change_resolution", resolution=WindowSize)

    def handle_events(self, event):
        self.win_layer.handle_events(event)
        self.ui_layer.handle_events(event)
        self.world_layer.handle_events(event)

    def update(self, context):
        self.win_layer.update(context)
        self.ui_layer.update(context)
        self.world_layer.update(context)

    def draw(self, _screen):
        self.world_layer.draw(_screen)
        self.ui_layer.draw(_screen)
        self.win_layer.draw(_screen)

    def enter(self):
        role_manager.load_into(scene=self)
        self.world_layer.window_update(role_manager.main_role.x, role_manager.main_role.y, True)

    def exit(self):
        self.world_layer.destroy()
        self.ui_layer.destroy()
        self.win_layer.destroy()


class LoginScene(Scene):
    def __init__(self, *args, **kwargs):
        Ref.__init__(self)

        self.scene_class_name = ""
        self.title = ""

        self.ui_layer = Root()

        self.music("music.wdf", "0x890BA81F")

        self.emit("change_resolution", resolution=(640, 480))

    def handle_events(self, event):
        self.ui_layer.handle_events(event)

    def update(self, context):
        self.ui_layer.update(context)

    def draw(self, _screen):
        self.ui_layer.draw(_screen)

    def enter(self):
        pass

    def exit(self):
        self.ui_layer.destroy()
