from core.ui.dialog import ModalDialog
from core.ui.text import Text
from core.ui.select import Select
from core.ui.static_node import StaticNode

from data.dialog import res
from settings import UI, WindowSize


class NPCDialog(ModalDialog):
    def __init__(self, npc_id, npc_name, conversion):
        self.npc_id = npc_id
        self.npc_name = npc_name
        self.conversion = conversion

        self.small_dialog = True

        super().__init__(**res[UI]["小对话框"], name="NPC_DIALOG", x=0, y=0)

        self.change_content()

    def change_content(self):
        self.clear_children()
        
        content = self.conversion.get()

        if content["options"] and len(content["options"]) > 5:
            self.set_bg(**res[UI]["大对话框"])
            self.small_dialog = False
        elif not self.small_dialog:
            self.set_bg(**res[UI]["小对话框"])
            self.small_dialog = True

        self.x = (WindowSize[0] - self.w) // 2
        self.y = (WindowSize[1] - self.h) // 5 * 3

        y = 20
        self.title = Text(content["lines"], x = 20, y = 20, w=500)
        self.add_child(self.title)
        y += self.title.h + 10

        self.select_ui = Select(content["options"], x = 20, y = y)
        self.add_child(self.select_ui)

        if int(self.npc_id) > 2000:
            was = 'npc/' + str(self.npc_id) + '.tga'
        else:
            was = 'hero/' + str(self.npc_id) + '.tga'
        self.figure = StaticNode(wdf="photo", was_hash=was, x=0)
        self.figure.y = -self.figure.h
        self.add_child(self.figure)
                
    def on_mouse_right_up(self, event): 
        if self.screen_rect.collidepoint(*event.pos):
            if not self.select(-1):
                self.useless = True
        event.handled = True

    def select(self, value):
        if self.conversion.proceed(value):
            self.change_content()
            return True
        self.useless = True
        return False
        