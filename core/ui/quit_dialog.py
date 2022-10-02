from core.ui.dialog import Confirm
from core.ui.label_button import LongLabelButton
from core.ui.text import Text


class QuitDialog(Confirm):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(name="quit_dialog", x=x, y=y, z=z)

        self.text = Text("确认退出游戏？ #32", 30, 20, self.w - 40, 60)
        self.add_child(self.text)

        self.quit_button = LongLabelButton(label="退出游戏", x=30, y=85)
        self.quit_button.click = lambda : self.notify("exit")
        self.add_child(self.quit_button)

        self.cancel_button = LongLabelButton(label="继续游戏", x=230, y=85)
        def cancel_click(): 
            self.hidden = True
        self.cancel_button.click = cancel_click
        self.add_child(self.cancel_button)

        self.return_button = LongLabelButton(label="到主画面", x=130, y=85)
        def return_click(): 
            self.emit("change_scene", scene_name="StartScene")
            self.hidden = True
        self.return_button.click = return_click
        self.add_child(self.return_button)
