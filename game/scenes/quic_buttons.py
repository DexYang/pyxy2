from core.ui.button import Button
from core.ui.react_button import ReactButton

from data.world.ui import res
from settings import UI, WindowSize


class 成就(Button):
    def click(self, *args, **kwargs):
        if not hasattr(self.parent, "成就窗口"):
            print("成就窗口不存在")


class 宝宝(Button):
    def click(self, *args, **kwargs):
        if not hasattr(self.parent, "宝宝窗口"):
            print("宝宝窗口不存在")


class 道具(Button):
    def click(self, *args, **kwargs):
        if not hasattr(self.parent, "道具窗口"):
            print("道具窗口不存在")


class 组队(ReactButton):
    def click(self, *args, **kwargs):
        if not hasattr(self.parent, "组队窗口"):
            print("组队窗口不存在")


class 攻击(Button):
    def click(self, *args, **kwargs):
        if not hasattr(self.parent, "攻击窗口"):
            print("攻击窗口不存在")


class 给予(Button):
    def click(self, *args, **kwargs):
        if not hasattr(self.parent, "给予窗口"):
            print("给予窗口不存在")


class 交易(ReactButton):
    def click(self, *args, **kwargs):
        if not hasattr(self.parent, "交易窗口"):
            print("交易窗口不存在")


class 坐骑(Button):
    def click(self, *args, **kwargs):
        if not hasattr(self.parent, "坐骑窗口"):
            print("坐骑窗口不存在")


class 宠物(Button):
    def click(self, *args, **kwargs):
        if not hasattr(self.parent, "宠物窗口"):
            print("宠物窗口不存在")


class 技能(Button):
    def click(self, *args, **kwargs):
        if not hasattr(self.parent, "技能窗口"):
            print("技能窗口不存在")


class 任务(Button):
    def click(self, *args, **kwargs):
        if not hasattr(self.parent, "任务窗口"):
            print("任务窗口不存在")


class 好友(ReactButton):
    def click(self, *args, **kwargs):
        if not hasattr(self.parent, "好友窗口"):
            print("好友窗口不存在")


class 帮派(Button):
    def click(self, *args, **kwargs):
        if not hasattr(self.parent, "帮派窗口"):
            print("帮派窗口不存在")


class 系统(Button):
    def click(self, *args, **kwargs):
        if not hasattr(self.parent, "系统窗口"):
            print("系统窗口不存在")


CLASS = {
    "成就": 成就,
    "宝宝": 宝宝,
    "道具": 道具,
    "组队": 组队,
    "攻击": 攻击,
    "给予": 给予,
    "交易": 交易,
    "坐骑": 坐骑,
    "宠物": 宠物,
    "技能": 技能,
    "任务": 任务,
    "好友": 好友,
    "帮派": 帮派,
    "系统": 系统
}


def get_quic_buttons():
    keys = list(res[UI]["button"].keys())
    x = WindowSize[0]
    y = WindowSize[1]
    buttons = []
    for k in range(len(keys) - 1, -1, -1):
        v = res[UI]["button"][keys[k]]
        static = CLASS[keys[k]](name=keys[k], **v)

        static.y = y - static.h
        static.x = x - static.w
        x -= static.w
        buttons.append(static)
    return buttons, x
