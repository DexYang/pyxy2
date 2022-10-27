
from core.ui.static_node import StaticNode
from data.dialog import res as dialog_res


class Dialog(StaticNode):
    def __init__(self, wdf, was_hash, name, x=0, y=0, z=0):
        super().__init__(wdf, was_hash, name, x, y, z)
        self.pressed = False

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
        if not event.processed and self.screen_rect.collidepoint(*event.pos):
            if self.parent.max_z != self.z:
                self.z = self.parent.max_z + 1
            self.pressed = True
            event.processed = True

    def on_mouse_motion(self, event): 
        if not event.processed and self.screen_rect.collidepoint(*event.pos):
            if self.pressed:
                self.rect.move_ip(event.rel[0], event.rel[1])
            event.processed = True

    def on_mouse_left_up(self, event): 
        self.pressed = False

    def on_mouse_right_up(self, event): 
        if self.screen_rect.collidepoint(*event.pos):
            self.hidden = True
            event.handled = True

class Confirm(Dialog):
    def __init__(self, name, x=0, y=0, z=0):
        super().__init__(**self.get_res(dialog_res, "confirm"), name=name, x=x, y=y, z=z)


class ModalDialog(Dialog):
    def __init__(self, wdf, was_hash, name, x=0, y=0, z=9999):
        super().__init__(wdf, was_hash, name, x, y, z)

    def on_mouse_left_down(self, event): 
        if not event.processed and self.screen_rect.collidepoint(*event.pos):
            self.pressed = True
        event.handled = True

    def on_mouse_motion(self, event): 
        if not event.processed and self.screen_rect.collidepoint(*event.pos):
            if self.pressed:
                self.rect.move_ip(event.rel[0], event.rel[1])
        event.handled = True

    def on_mouse_left_up(self, event): 
        self.pressed = False
        self.handled = True

    def on_mouse_right_up(self, event): 
        if self.screen_rect.collidepoint(*event.pos):
            self.hidden = True
        event.handled = True
