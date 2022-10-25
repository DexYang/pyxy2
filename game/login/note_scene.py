from core.scene import LoginScene
from data.login.note_scene import res
from settings import UI
from core.ui.button import Button
from core.ui.static_node import StaticNode
from core.ui.text import Text
import os


class NoteScene(LoginScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scene_class_name = "游戏公告"
        self.title = "游戏公告"

        f = open(os.getcwd() + '/res/note.txt', 'r', encoding='utf-8')
        text = f.read()
        f.close()

        backgorund = StaticNode(name="backgorund", **res[UI]["static"]["backgorund"])
        def right_click_bg(event):
            self.emit("change_scene", scene_name="LoginScene") 
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
        self.backbtn.click = lambda : self.emit("change_scene", scene_name="LoginScene") 
        self.ui_layer.add_child(self.backbtn)

        self.note = Text(text=text, font_size=16, x=33, y=65, w=485, h=350, z=100)
        self.ui_layer.add_child(self.note)