from core.state import State
from core.res_manager import res_manager


class AnimatedState(State):
    res_index = 'normal'
    with_mask = False

    def __init__(self, wdf_name, was_hash):
        super().__init__()
        self.ani = res_manager.get(wdf_name, was_hash)

    def update(self, context):
        one_loop = self.ani.update(context.get_current_time())
        self.ani.set_direction(self.parent.direction)
        return one_loop

    def draw(self, screen, x, y):
        self.ani.draw(screen, x, y)

    def bind(self, parent):
        self.parent = parent
        self.ani.frame = 0

    def change_state(self, state_name):
        self.emit(event_name="change_state", target_id=self.parent.id, state_name=state_name)
