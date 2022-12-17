import pygame as pg
import weakref
from pygame.locals import Rect
from core.ref import Ref
from core.ui.text import Text


class Sprite(Ref):
    def __init__(self, x=0, y=0):
        super().__init__()

        self.rect = Rect((0, 0), (0, 0))
        self.screen_rect = Rect((0, 0), (0, 0))
        self.x = x
        self.y = y
        self.z = 0

        self.useless = False

        self.hover = False

        self.surface = None

        self._parent = None
        self.children = {}
        self.children_upper = {}
        self.children_lower = {}
        self.children_text = {}

    @property
    def parent(self):
        return None if self._parent is None else self._parent()

    @parent.setter
    def parent(self, node):
        self._parent = weakref.ref(node)

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
        self.update_children(context)

    def update_children(self, context):
        if not self.children:
            return
        for child in list(self.children.values()):
            child.update(context)
            if child.useless:
                child.parent = None
                self.children.pop(child.name)
                self.children_upper.pop(child.name)
                self.children_lower.pop(child.name)
                child.destroy()

    def _draw(self, screen):
        screen.blit(self.surface, self.screen_rect)

    def draw(self, screen):
        if not self.children:
            self._draw(screen)
        else:
            for child in list(self.children_lower.values()):
                child.draw(screen)
            self._draw(screen)
            for child in list(self.children_upper.values()):
                child.draw(screen)

    def draw_text(self, screen):
        for child in list(self.children_text.values()):
            child.draw(screen)
            
    def add_child(self, node, override=False):
        if node.name not in self.children or override:
            node.parent = self
            self.children[node.name] = node
            if isinstance(node, Text):
                self.children_text[node.name] = node
            elif node.z < 0:
                self.children_lower[node.name] = node
            else:
                self.children_upper[node.name] = node
