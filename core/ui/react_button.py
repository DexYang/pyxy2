from core.animation import Animation
from core.res_manager import res_manager
from core.ui.button import Button


class ReactButton(Button):
    def __init__(self, wdf, was_hash, react_wdf, react_was_hash, name, value=None, x=0, y=0, z=100):
        super().__init__(wdf, was_hash, name, value, x, y, z)

        self.react_ani = Animation(res_manager.get(react_wdf, react_was_hash))
        self.react = False

    def update(self, context): 
        if self.hidden:
            return
        self.screen_rect = self.rect.move(*self.get_parent_screen_xy())
        if self.react:
            self.react_ani.update(context)

    def draw(self, screen):
        if self.react:
            self.react_ani.draw(screen, self.screen_rect.x, self.screen_rect.y)
        elif self.pressed:
            screen.blit(self.hover_pic, self.screen_rect)
        elif self.hover:
            screen.blit(self.pressed_pic, self.screen_rect)
        else:
            screen.blit(self.normal_pic, self.screen_rect)

