from core.ui.node import Node
from core.animation import Animation
from core.res_manager import res_manager, WAS
import pygame
from utils.scale9 import scale_horizontal


class StaticNode(Node):
    def __init__(self, wdf, was_hash, name=None, x=0, y=0, z=0):

        self.wdf = wdf
        self.was_hash = was_hash

        self.surface = None
        self.item = res_manager.get(wdf, was_hash)
        if isinstance(self.item, WAS):
            self.item = Animation(self.item)
            self.surface = self.item.get_current_frame().surface
        else:
            self.surface = self.item

        super().__init__(name, x, y, self.surface.get_width(), self.surface.get_height(), z)

    def draw(self, screen):
        if self.hidden:
            return
        screen.blit(self.surface, self.screen_rect)


class StaticText(StaticNode):
    def update(self, context):
        if self.hidden:
            return
        self.screen_rect = self.rect.move(*self.get_parent_screen_xy())
        self.update_children(context)

    def draw(self, screen):
        if self.hidden:
            return
        screen.blit(self.surface, self.screen_rect)
        self.draw_children(screen)
        
        
class ExtWidthStatic(StaticNode):
    def __init__(self, wdf, was_hash, name=None, x=0, y=0, z=0, w=0):
        super().__init__(wdf, was_hash, name, x, y, z)
        
        if w >= self.w:
            self.w = w
            self.surface = scale_horizontal(self.surface, w)
            