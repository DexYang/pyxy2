import pygame as pg
from pygame.locals import Rect
from core.sprite import Sprite
import weakref
from math import floor


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

        self.sort_table = []
        self.sample_gap = 10

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
        sample = [x for x in range(0, self.width, self.sample_gap)]
        self.sort_table = []
        for x in sample:
            self.sort_table.append(self.calc_sort_point(x))
        # TODO
        font = pg.font.SysFont("simsun", 16)
        self.font_surf = font.render((str(self.start_x)+":"+str(self.start_y)), True, (255, 0, 0))

    def update(self, context):
        left, top = context.get_left_top()
        self.screen_rect = self.rect.move(-left, -top)

    def draw(self, screen):
        # mask (255, 255, 255, alpha)
        # TODO
        pg.draw.rect(screen, (255, 0, 0), self.screen_rect, 1)
        screen.blit(self.font_surf, self.screen_rect)
        
        screen.blit(self.surface, self.screen_rect, special_flags=pg.BLEND_RGBA_MIN)

    def collide(self, x, y):
        return self.surface.get_at((x, y)).a == 1

    def calc_sort_point(self, x):
        top = 0
        bottom = self.height - 1
        mid = (top + bottom) // 2
        while bottom - top > 1:
            mid = (top + bottom) // 2
            if self.surface.get_at((x, mid)).a == 1:
                bottom = mid
            else:
                top = mid
        return mid + 1

    def calc_sort_z(self, char_rect, x, y):  # 判断char是否踩在mask.a == 1的区域， x, y为世界坐标
        if self.rect.y < y < self.z:
            if self.rect.colliderect(char_rect):
                rx = x - self.rect.x
                ry = y - self.rect.y
                if 0 <= rx < self.width:
                    x = floor(rx / 10)
                    return ry > self.sort_table[x]
                elif rx < 0: 
                    return ry > self.sort_table[0]
                else: 
                    return ry > self.sort_table[-1]
        return False
