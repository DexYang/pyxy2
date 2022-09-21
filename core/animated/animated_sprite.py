import pygame as pg

from utils.logger import logger
from core.sprite import Sprite
from core.animated.animated_state import AnimatedState


class AnimatedSprite(Sprite):
    INIT_STATE = "normal"
    STATES_CLASS = {
        "normal": AnimatedState
    }

    RES_INFO = None

    def __init__(self, x, y):
        super().__init__(x, y)

        self.direction = 0

        self.is_mouse_over = False

        self.STATES = {}
        self.state_name = ""
        self.state = None

        self.change_state(self.INIT_STATE)

    def on_change_state(self, event):
        if event.target_id == self.id:
            event.handled = True
            self.change_state(event.state_name)

    def change_state(self, state_name):
        if state_name == self.state_name:
            return
        if state_name not in self.STATES:  # 状态未初始化
            if state_name not in self.STATES_CLASS:
                logger.info("state doesn't exists:" + state_name)
                return
            state_class = self.STATES_CLASS[state_name]
            wdf_name, was_hash = self.RES_INFO[state_class.res_index]
            self.STATES[state_name] = state_class(wdf_name, was_hash)
        self.state = self.STATES[state_name]
        self.state.bind(self)
        self.state_name = state_name

    def update(self, context):
        self.state.update(context)
        left, top = context.get_left_top()
        self.screen_rect = self.rect.move(-left, -top)
        self.z = self.rect.y

    def draw(self, screen):
        self.state.draw(screen, self.screen_rect.x, self.screen_rect.y)
