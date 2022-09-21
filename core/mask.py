import pygame as pg
from pygame.locals import Rect
from core.sprite import Sprite
import weakref


bright = pg.Surface((400, 400), flags=pg.SRCALPHA)
bright.fill((250, 80, 80, 0))


class Mask(Sprite):
    def __init__(self, mask_index, start_x, start_y, width, height):
        super().__init__()
        self.surface = None

        self.mask_index = mask_index
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.rect = Rect(start_x, start_y, width, height)

        self.z = self.rect.y + self.rect.height

        self.requested = False
        self.received = False

        self._parent = None

    @property
    def parent(self):
        return None if self._parent is None else self._parent()

    @parent.setter
    def parent(self, node):
        self._parent = weakref.ref(node)

    def load_surface(self):
        self.surface = pg.image.frombuffer(
            self.parent.map.get_mask_rgba(self.mask_index, self.width * self.height * 4),
            (self.width, self.height), "RGBA")

    def update(self, context):
        left, top = context.get_left_top()
        self.screen_rect = self.rect.move(-left, -top)

    def draw(self, screen):
        # mask (255, 255, 255, alpha)
        screen.blit(self.surface, self.screen_rect, special_flags=pg.BLEND_RGBA_MIN)

    def collide(self, x, y):
        return self.surface.get_at((x, y)).a == 1
