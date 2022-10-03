from core.ui.node import Node
from core.animation import Animation
from core.res_manager import res_manager


class Button(Node):
    def __init__(self, wdf, was_hash, name, x=0, y=0, z=100):
        

        self.wdf = wdf
        self.was_hash = was_hash

        self.hover = False
        self.pressed = False

        self.ani = Animation(res_manager.get(wdf, was_hash))

        super().__init__(name, x, y, self.ani.width, self.ani.height, z)

        self.normal_pic = self.ani.frames[0][0].surface
        self.hover_pic = self.ani.frames[0][1].surface
        self.pressed_pic = self.ani.frames[0][2].surface

    def reset(self):  # 重置内部状态
        self.focus = False
        self.hover = False

    def draw(self, screen):
        if self.pressed:
            screen.blit(self.hover_pic, self.screen_rect)
        elif self.hover:
            screen.blit(self.pressed_pic, self.screen_rect)
        else:
            screen.blit(self.normal_pic, self.screen_rect)

    def on_mouse_motion(self, event): 
        if not event.processed:
            if self.is_in(event.pos): 
                self.hover = True
                event.processed = True
                self.emit("change_mouse_state", state_name = "pointer")
                return
        if self.hover:
            self.emit("change_mouse_state", state_name = "normal")
        self.hover = False
        
    def on_mouse_left_down(self, event): 
        if not event.processed and self.is_in(event.pos): 
            self.pressed = True
            event.processed = True
        
    def on_mouse_left_up(self, event): 
        if not event.processed and self.pressed and self.is_in(event.pos): 
            event.processed = True
            self.click()
            self.play("sound.wdf", "0x4F8F2281")
        self.pressed = False

    def click(self, *args, **kwargs):
        pass

    