from core.animated.npc import NPC
from game.tasks.task_manager import task_manager
from core.role_manager import role_manager


class WorldNPC(NPC):

    TOUCH_TASK = False

    def on_mouse_left_up(self, event):
        if not event.processed:
            if self.get_at(*event.pos):
                event.handled = True
                if self.TOUCH_TASK:
                    _type, _action = task_manager.touch(self.NPC_NAME)
                    if _type:
                        if _type == "对话":
                            self.open_dialog(_action)
                        return
                self.response()