import pygame as pg
from pygame.locals import Rect
from core.ref import Ref


class Sprite(Ref):
    def __init__(self, x=0, y=0):
        super().__init__()

        self.rect = Rect((0, 0), (0, 0))
        self.screen_rect = Rect((0, 0), (0, 0))
        self.x = x
        self.y = y
        self.z = 0

        self.pre = None
        self.next = None
        self.useless = False

        self.hover = False

        self.surface = None

    @property
    def x(self):  # x y为世界坐标，因为ani在draw时，已经减去锚点，实际上xy是人物锚点（人物脚底）
        return self.rect.x

    @x.setter
    def x(self, x):
        self.rect.x = x

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, y):
        self.rect.y = y

    def update(self, context):
        left, top = context.get_left_top()
        self.screen_rect = self.rect.move(-left, -top)
        self.z = self.rect.y

    def draw(self, screen):
        screen.blit(self.surface, self.screen_rect)
