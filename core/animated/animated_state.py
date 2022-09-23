from core.state import State
from core.res_manager import res_manager
from core.animation import Animation
import pygame

class AnimatedState(State):
    state_type = "normal"
    state_name = 'normal'
    with_mask = False
    animation_rate = 100
    

    def __init__(self, wdf_name, was_hash):
        super().__init__()
        self.ani = Animation(res_manager.get(wdf_name, was_hash), self.animation_rate)

    def update(self, context):
        one_loop = self.ani.update(context.get_current_time())
        self.ani.set_direction(self.parent.direction)
        return one_loop

    def draw(self, screen, x, y, bright):
        self.ani.draw(screen, x, y, bright)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x - self.ani.key_x, y - self.ani.key_y, self.ani.width, self.ani.height), 1)

    def bind(self, parent):
        self.parent = parent
        self.ani.frame = 0

    def change_state(self, state_name):
        self.parent.change_state(state_name)
