from core.ui.dialog import ModalDialog
from core.ui.text import Text
from core.ui.text_button import TextButton
from core.ui.static_node import StaticNode

from data.dialog import res
from settings import UI, WindowSize


class NPCDialog(ModalDialog):
    def __init__(self, npc_id, npc_name, title, options):
        if options and len(options) > 3:
            super().__init__(**res[UI]["大对话框"], name="NPC_DIALOG", x=0, y=0)
        else:
            super().__init__(**res[UI]["小对话框"], name="NPC_DIALOG", x=0, y=0)

        self.x = (WindowSize[0] - self.w) // 2
        self.y = (WindowSize[1] - self.h) // 5 * 3

        y = 20
        self.title = Text(title, x = 20, y = 20, w=500)
        self.add_child(self.title)
        y += self.title.h + 10

        if options:
            for k, v in options.items():
                text_button = TextButton(k, x = 20, y = y)
                text_button.click = v
                self.add_child(text_button)
                y += text_button.text.h + 5

        if int(npc_id) > 2000:
            was = 'npc/' + str(npc_id) + '.tga'
        else:
            was = 'hero/' + str(npc_id) + '.tga'
        self.figure = StaticNode(wdf="photo", was_hash=was, x=0)
        self.figure.y = -self.figure.h
        self.add_child(self.figure)

                
    def on_mouse_right_up(self, event): 
        if self.screen_rect.collidepoint(*event.pos):
            self.useless = True
        event.handled = True

        