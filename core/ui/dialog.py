
from core.ui.static_node import StaticNode
from data.dialog import res as dialog_res


class Dialog(StaticNode):
    def __init__(self, wdf, was_hash, name, x=0, y=0, z=0):
        super().__init__(wdf, was_hash, name, x, y, z)
        self.pressed = False
        self._x = 0
        self._y = 0

    def update(self, context):
        if self.hidden:
            return
        self.screen_rect = self.rect.move(*self.get_parent_screen_xy())
        self.update_children(context)

    def draw(self, screen):
        if self.hidden:
            return
        screen.blit(self.surface, self.screen_rect)
        self.draw_children(screen)

    def on_mouse_left_down(self, event): 
        if self.screen_rect.collidepoint(*event.pos):
            self.pressed = True
            event.handled = True
            self._x = event.pos[0]
            self._y = event.pos[1]

    def on_mouse_motion(self, event): 
        if self.screen_rect.collidepoint(*event.pos):
            if self.pressed:
                delta_x = event.pos[0] - self._x
                delta_y = event.pos[1] - self._y
                self.rect.move_ip(delta_x, delta_y)
                self._x = event.pos[0]
                self._y = event.pos[1]
            event.processed = True

    def on_mouse_left_up(self, event): 
        self.pressed = False

    def on_mouse_right_down(self, event): 
        if self.screen_rect.collidepoint(*event.pos):
            self.hidden = True
            event.handled = True
            

class Confirm(Dialog):
    def __init__(self, name, x=0, y=0, z=0):
        super().__init__(**self.get_res(dialog_res, "confirm"), name=name, x=x, y=y, z=z)