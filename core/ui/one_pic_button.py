from core.ui.button import Button
from core.ui.node import Node
from core.res_manager import res_manager, WAS
from core.animation import Animation
import pygame


class OnePicButton(Button):
    def __init__(self, wdf, was_hash, name=None, selected=False, x=0, y=0, z=100):
        
        self.wdf = wdf
        self.was_hash = was_hash

        self.hover = False
        self.pressed = False
        self.selected = selected

        self.item = res_manager.get(wdf, was_hash)
        if isinstance(self.item, WAS):
            self.item = Animation(self.item)
            self.surface = self.item.get_current_frame().surface
        else:
            self.surface = self.item
            
        super(Button, self).__init__(name, x, y, self.surface.get_width(), self.surface.get_height(), z)

    def draw(self, screen):
        draw_rect = self.screen_rect.move(1, 1) if self.pressed else self.screen_rect
        screen.blit(self.surface, draw_rect)
        if self.selected:
            pygame.draw.rect(screen, (255, 0, 0), draw_rect, width=1)

