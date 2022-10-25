from core.ui.static_node import StaticNode
from core.role_manager import role_manager

from data.exp import 人物经验库, 召唤兽经验库
from data.world.ui import res 
from settings import UI, WindowSize


class ShrinkNode(StaticNode):
    index = ""

    def __init__(self, wdf, was_hash, name=None, x=0, y=0, z=0):
        super().__init__(wdf, was_hash, name, x, y, z)

        self.surface_rect = self.surface.get_rect()
        self.shrink_rect = self.surface_rect.copy()

        self.ani_surface = None
        self._shrink = False
        self._shrink_down = 0

        self.change()

    def draw(self, screen):
        if self.hidden:
            return
        if self._shrink:
            self.ani_surface.set_alpha(self._shrink_down)
            self._shrink_down -= 25
            screen.blit(self.ani_surface, self.screen_rect)
            if self._shrink_down < 0:
                self._shrink = False
                self.ani_surface = None
        screen.blit(self.surface, self.screen_rect, self.shrink_rect)

    def numerator(self):
        return role_manager.main_role.data[self.index]

    def denominator(self):
        return role_manager.main_role.data["最大"+self.index]

    def change(self):
        self.shrink_rect.w = min(self.numerator() / self.denominator(), 1) * self.surface_rect.w

    def shrink(self):
        self._shrink = True
        self._shrink_down = 255
        self.ani_surface = self.surface.subsurface(self.shrink_rect)
        self.change()

    def on_change_status(self, event):
        self.change()


class 气血条(ShrinkNode):
    index = "气血"

class 法力条(ShrinkNode):
    index = "法力"

class 经验条(ShrinkNode):
    index = "经验"

    def denominator(self):
        return 人物经验库[role_manager.main_role.data["转生"]][role_manager.main_role.data["等级"]]


class 召唤兽(ShrinkNode):
    def numerator(self):
        data = role_manager.main_role.data
        return data["召唤兽"][data["已选召唤兽"]][self.index]

    def denominator(self):
        data = role_manager.main_role.data
        return data["召唤兽"][data["已选召唤兽"]]["最大"+self.index]

    def change(self):
        data = role_manager.main_role.data
        if data["已选召唤兽"] == -1 or len(data["召唤兽"]) == 0:
            self.hidden = True
            return
        self.shrink_rect.w = min(self.numerator() / self.denominator(), 1) * self.surface_rect.w


class 召唤兽气血条(召唤兽):
    index = "气血"

class 召唤兽法力条(召唤兽):
    index = "法力"

class 召唤兽经验条(召唤兽):
    index = "经验"

    def denominator(self):
        data = role_manager.main_role.data
        return 召唤兽经验库[data["召唤兽"][data["已选召唤兽"]]["等级"]]