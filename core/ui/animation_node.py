from core.ui.node import Node
from core.animation import Animation
from core.res_manager import res_manager


class AnimationNode(Node):

    def __init__(self, wdf, was_hash, name=None, x=0, y=0, z=0, animation_rate=100):

        self.wdf = wdf
        self.was_hash = was_hash

        self.animation_rate = animation_rate

        self.ani = Animation(res_manager.get(wdf, was_hash), self.animation_rate)

        super().__init__(name, x, y, self.ani.width, self.ani.height, z)

    def update(self, context):
        if self.hidden:
            return
        self.screen_rect = self.rect.move(*self.get_parent_screen_xy())
        self.ani.update(context.get_current_time())

    def draw(self, screen):
        if self.hidden:
            return
        self.ani.draw(screen, self.screen_rect.x, self.screen_rect.y)