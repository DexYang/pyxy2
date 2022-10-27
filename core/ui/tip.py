from math import ceil, floor
from core.ui.static_node import StaticNode
from core.ui.text import Text
import pygame
from pygame import Rect
from utils.scale9 import scale9_surf


TIP_POOL = {
    
}


class Tip(StaticNode):
    def __init__(self, text, x=0, y=0, z=0):
        super().__init__("gires.wdf", "0x8D580095", None, x, y, z)
        self.text = Text(text, w=280)
        self.add_child(self.text)

        # 宽度320固定，高度动态
        self.w = 320
        self.h = floor((self.text.h + 40) / 10) * 10
        if self.h in TIP_POOL:
            self.surface = TIP_POOL[self.h]
        else:
            self.surface = scale9_surf(self.surface, self.w, self.h)
            TIP_POOL[self.h] = self.surface

        self.rect.width = self.w
        self.rect.height = self.h

        self.text.x = (320 - self.text.max_width) // 2 + 10
        self.text.y = 12 if self.text.first_line_emoji else 22

        self.start_time = 0
        self.just_init = True

        self.pressed = False

    def update(self, context):
        if self.just_init:
            self.start_time = context.get_current_time()
            self.just_init = False
        self.screen_rect = self.rect.move(*self.get_parent_screen_xy())
        self.update_children(context)
        if context.get_current_time() - self.start_time > 5000:
            self.useless = True

    def draw(self, screen):
        if self.hidden:
            return
        screen.blit(self.surface, self.screen_rect)
        self.draw_children(screen)

    def on_mouse_left_up(self, event):
        if not event.processed and self.screen_rect.collidepoint(*event.pos):
            self.useless = True
            self.pressed = False
            event.processed = True

    def on_mouse_left_down(self, event): 
        if not event.processed and self.screen_rect.collidepoint(*event.pos):
            self.pressed = True
            event.processed = True

    def on_mouse_motion(self, event): 
        if not event.processed and self.screen_rect.collidepoint(*event.pos):
            if self.pressed:
                self.rect.move_ip(event.rel[0], event.rel[1])
            event.processed = True

    def on_mouse_right_up(self, event): 
        if self.screen_rect.collidepoint(*event.pos):
            self.useless = True
            event.handled = False