from core.ui.node import Node
from core.animation import Animation
from core.res_manager import res_manager, WAS
import pygame


class StaticNode(Node):
    def __init__(self, wdf, was_hash, name, x=0, y=0, z=0, animation_rate=100):

        self.wdf = wdf
        self.was_hash = was_hash

        self.surface = None
        self.item = res_manager.get(wdf, was_hash)
        if isinstance(self.item, WAS):
            self.item = Animation(self.item, animation_rate)
            self.surface = self.item.get_current_frame().surface
        else:
            self.surface = self.item

        super().__init__(name, x, y, self.surface.get_width(), self.surface.get_height(), z)

    def draw(self, screen):
        if self.hidden:
            return
        screen.blit(self.surface, self.screen_rect)