import imp
from core.ui.dialog import Dialog, StaticNode

from data.dialog import res
from settings import UI

from utils.scale9 import scale9_combination
from core.ui.button import Button


class CombinationDialog(Dialog):
    def __init__(self, name, x=0, y=0, w=0, h=0, z=0):
        super(StaticNode, self).__init__(name, x=x, y=y, w=w, h=h, z=z)

        self.pressed = False

        上 = res[UI]["combination"]["上"]
        下 = res[UI]["combination"]["下"]
        左 = res[UI]["combination"]["左"]
        右 = res[UI]["combination"]["右"]
        左上 = res[UI]["combination"]["左上"]
        左下 = res[UI]["combination"]["左下"]
        右上 = res[UI]["combination"]["右上"]
        右下 = res[UI]["combination"]["右下"]
        底 = res[UI]["combination"]["底"]
        花 = res[UI]["combination"].get("花", res[UI]["combination"]["底"])

        self.surface = scale9_combination(w, h, 底=底, 花=花,
                                         上=上, 下=下, 左=左, 右=右, 
                                         左上=左上, 左下=左下, 右上=右上, 右下=右下)

        self.关闭 = Button(name="关闭", **res[UI]["combination"]["关闭"])
        self.关闭.x = w - self.关闭.w
        def 关闭click():
            self.hidden = True
        self.关闭.click = 关闭click
        self.add_child(self.关闭)
