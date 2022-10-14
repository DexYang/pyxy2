from core.animated.animated_sprite import AnimatedSprite
import pygame
from core.role_manager import role_manager


class Portal(AnimatedSprite):
    WDF = "mapani.wdf"
    WAS = "change_point.tcp"

    def __init__(self, x, y, map_id, tx, ty):
        super().__init__(x, y)

        self.map_id = map_id
        self.tx = tx
        self.ty = ty

        self.collide_rect = pygame.Rect(self.x - 25, self.y - 25, 50, 50)

        self.count = 0

    def update(self, context):
        super().update(context)
        if self.count > 5:
            self.count = -1
            if self.collide_rect.collidepoint(role_manager.main_role.x, role_manager.main_role.y):
                role_manager.change_world(self.map_id, self.tx, self.ty)
        self.count += 1