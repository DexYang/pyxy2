from core.ui.node import Blank
from game.scenes.windows.npc_dialog import NPCDialog


class WindowLayer(Blank):
    def __init__(self, name=None, x=0, y=0, w=0, h=0, z=0):
        super().__init__(name, x, y, w, h, z)
        self.max_z = 0

    def add_child(self, node):
        super().add_child(node)
        node.z = self.max_z + 1
        self.max_z += 1

    def on_open_dialog(self, event):
        npc_dialog = NPCDialog(event.npc_id, event.npc_name, event.conversation)
        self.add_child(npc_dialog)
        event.handled = True