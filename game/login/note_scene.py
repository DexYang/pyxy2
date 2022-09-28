from core.scene import LoginScene
from data.login.note_scene import res
from settings import UI
from core.ui.button import Button
from core.ui.static_node import StaticNode


class NoteScene(LoginScene):
    def __init__(self):
        super().__init__()

        self.scene_class_name = "游戏公告"
        self.title = "游戏公告"

        backgorund = StaticNode(name="backgorund", **res[UI]["static"]["backgorund"])
        def right_click_bg(event):
            self.emit("change_scene", scene_name="OldChangAnScene") 
            event.handled = True
        backgorund.on_mouse_right_up = right_click_bg
        self.ui_layer.add_child(backgorund)


        buttons = res[UI]["buttons"]
        self.lup = Button(name="lup", **buttons["lup"])
        self.lup.click = lambda : print("lup")
        self.ui_layer.add_child(self.lup)

        self.ldown = Button(name="ldown", **buttons["ldown"])
        self.ldown.click = lambda : print("ldown")
        self.ui_layer.add_child(self.ldown)

        self.backbtn = Button(name="backbtn", **buttons["backbtn"])
        self.backbtn.click = lambda : print("backbtn")
        self.ui_layer.add_child(self.backbtn)
