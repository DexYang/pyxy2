from abc import abstractmethod
from inspect import isclass
import pygame as pg

from core.sprite import Sprite
from core.animated.animated_state import AnimatedState


class AnimatedSprite(Sprite):
    INIT_STATE = "normal"
    STATES_CLASS = {
        "normal": AnimatedState
    }

    WDF = ""
    WAS = ""

    def __init__(self, x, y):
        super().__init__(x, y)

        self.direction = 0

        self.is_mouse_over = False

        self.STATES = {}
        self.state_name = ""
        self.state = None

        self.change_state(self.INIT_STATE)

    def get_res(self, *args, **kwargs):
        return self.WDF, self.WAS

    def on_change_state(self, event):
        if event.target_id == self.id:
            event.handled = True
            self.change_state(event.state_name)

    def change_state(self, state_name):
        if state_name == self.state_name:
            return
        if state_name not in self.STATES:  # 状态未初始化
            if state_name not in self.STATES_CLASS:
                self.log.info("state doesn't exists:" + state_name)
                return
            item = self.STATES_CLASS[state_name]
            if isclass(item):
                wdf_name, was_hash = self.get_res(item.state_name, item.state_type)
                self.STATES[state_name] = item(wdf_name, was_hash)
            else:
                self.STATES[state_name] = item
        self.state = self.STATES[state_name]
        self.state.bind(self)
        self.state_name = state_name

    def update(self, context):
        self.state.update(context)
        left, top = context.get_left_top()
        self.screen_rect = self.rect.move(-left, -top)
        self.z = self.rect.y

    def draw(self, screen):
        self.state.draw(screen, self.screen_rect.x, self.screen_rect.y, self.hover)

    def get_ani_screen_rect(self):
        return pg.Rect(self.screen_rect.x - self.state.ani.key_x, self.screen_rect.y - self.state.ani.key_y, self.state.ani.width, self.state.ani.height)

    
