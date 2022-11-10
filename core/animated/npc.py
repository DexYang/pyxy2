from core.animated.animated_sprite import AnimatedSprite
from core.animated.animated_state import AnimatedState
from core.ui.text import Text


class NPC(AnimatedSprite):
    INIT_STATE = "stand"
    STATES_CLASS = {
        "stand": AnimatedState
    }

    WDF = "shape.wdf"
    WAS = "char/{:04d}/{}.tcp"

    CHAR_ID = 3001

    X = 0
    Y = 0
    DIRECTION = 0

    def __init__(self):
        super().__init__(self.X, self.Y)
        self.direction = self.DIRECTION

        self.name = Text("#Y#d"+self.__class__.__name__, w=100, h=16, font_size=16, shadow=True, font_name='font/AdobeSong.ttf')
        self.name.x = - self.name.max_width / 2
        self.name.y = 20
        self.add_child(self.name)

    def get_res(self, *args, **kwargs):
        return self.WDF, self.WAS.format(self.CHAR_ID, self.INIT_STATE)

    def on_mouse_motion(self, event):
        if not event.processed:
            if self.get_at(*event.pos):
                self.hover = True
                event.processed = True
                return
        self.hover = False

    def get_at(self, x, y):
        return self.get_ani_screen_rect().collidepoint(x, y)

    def on_mouse_left_down(self, event):
        self.emit("open_dialog", **self.get_dialog_content())
        event.handled = True

    def get_dialog_content(self):
        return {
            "title": "",
            "options": [

            ]
        }