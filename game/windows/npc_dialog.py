from core.ui.dialog import ModalDialog

from data.dialog import res
from settings import UI, WindowSize


class NPCDialog(ModalDialog):
    def __init__(self, npc_id, npc_name, title, options):
        super().__init__(**res[UI]["大对话框"], name="NPC_DIALOG", x=0, y=0)

        self.x = (WindowSize[0] - self.w) // 2
        self.y = (WindowSize[1] - self.h) // 2

        