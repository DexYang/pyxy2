import pygame as pg
from pygame.locals import Rect
from core.ref import Ref


class Node(Ref):
    def __init__(self, name=None, x=0, y=0, w=0, h=0, z=0):
        super().__init__()

        self.name = name if name else str(self.id)
        
        self.rect = Rect((x, y), (w, h))  # 相对坐标
        self.x = x
        self.y = y
        self.screen_rect = Rect((x, y), (w, h))
        self._z = z
        self.w = w
        self.h = h

        self.useless = False
        self.hidden = False

        self.parent = None
        self.deep = 0

        self.children = {}
        self.children_z = {}

        self.focus = False

    @property
    def x(self):
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

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        if self.parent:
            self.parent.child_z_update(self, self._z, z)
        self._z = z

    def handle_events(self, event):
        if self.hidden:
            return
        for child in self.children.values():
            child.handle_events(event)
            if event.handled == True:
                return
        return self.handle_event(event)

    def update_children(self, context):
        if self.hidden:
            return
        for child in self.children.values():
            child.update(context)
            if child.useless:
                child.parent = None
                self.children.pop(child.name)

    def draw_children(self, screen):
        if self.hidden:
            return

        z_order = list(self.children_z.keys())
        z_order.sort()

        for z in z_order:
            for child in self.children_z[z].values():
                child.draw(screen)

    def update(self, context): 
        if self.hidden:
            return
        self.screen_rect = self.rect.move(*self.get_parent_screen_xy())

    def draw(self, screen):
        if self.hidden:
            return

    def add_child(self, node):
        if isinstance(node, Node):
            if node.name not in self.children:
                node.parent = self
                node.deep = self.deep + 1
                self.children[node.name] = node
                if node.z not in self.children_z:
                    self.children_z[node.z] = {}
                self.children_z[node.z][node.name] = node

    def clear_children(self):
        for child in self.children.values():
            child.clear_children()
        self.children.clear()
        self.children_z.clear()

    def child_z_update(self, node, old_z, new_z):
        self.children_z[old_z].pop(node.name)
        if len(self.children_z[old_z]) == 0:
            self.children_z.pop(old_z)
        if new_z not in self.children_z:
            self.children_z[new_z] = {}
        self.children_z[new_z][node.name] = node

    def __del__(self):
        self.clear_children()
        super().__del__()

    def reset(self):  # 重置内部状态
        self.focus = False

    def get_parent_screen_xy(self): 
        if self.parent:
            return self.parent.screen_rect.topleft
        return 0, 0

    def is_in(self, pos): 
        return self.screen_rect.collidepoint(*pos)

class Root(Node):
    def __init__(self):
        super().__init__("root")

    def update(self, context): 
        self.update_children(context)

    def draw(self, screen): 
        self.draw_children(screen)