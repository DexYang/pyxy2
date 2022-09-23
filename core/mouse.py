from core.animated.animated_sprite import AnimatedSprite
from core.animated.animated_state import AnimatedState


class MouseState(AnimatedState):
    animation_rate = 150

class Mouse(AnimatedSprite):
    INIT_STATE = "normal"
    STATES_CLASS = {
        "normal": MouseState("gires.wdf", "cursor/a.tca"),
        "input": MouseState("gires.wdf", "cursor/b.tca"),
        "pointer": MouseState("gires.wdf", "cursor/c.tca"),
        "disable": MouseState("gires.wdf", "cursor/d.tca"),
        "friend": MouseState("gires.wdf", "cursor/g.tca"),
        "trade": MouseState("gires.wdf", "cursor/i.tca"),
        "magic": MouseState("gires.wdf", "cursor/k.tca"),
        "give": MouseState("gires.wdf", "cursor/m.tca"),
        "fight": MouseState("gires.wdf", "cursor/o.tca"),
        "defend": MouseState("gires.wdf", "cursor/q.tca"),
        "catch": MouseState("gires.wdf", "cursor/s.tca"),
        "team": MouseState("gires.wdf", "cursor/u.tca"),
        "props": MouseState("gires.wdf", "cursor/v.tca")
    }

    def update(self, context):
        self.state.update(context)
        self.screen_rect.x, self.screen_rect.y = context.get_mouse_pos()

    def on_change_mouse_state(self, event):
        self.change_state(event.state_name)
        event.handled = True

    def get_res(self):
        pass
