from core.ui.button import Button
from core.ui.text import TextWrapper
from data.button import res
from settings import UI



class LabelButton(Button):
    def __init__(self, wdf, was_hash, label, value=None, x=0, y=0, z=100):
        super().__init__(wdf, was_hash, label, value, x, y, z)

        self.label = TextWrapper(label, color=(210, 210, 0), fontname="font/fzls.ttf", fontsize=18)
        self.label.x = (self.w - self.label.len) // 2
        self.label.y = 2

    def update(self, context): 
        if self.hidden:
            return
        self.screen_rect = self.rect.move(*self.get_parent_screen_xy())
        self.label.screen_rect = self.label.rect.move(*self.screen_rect.topleft)

    def draw(self, screen):
        if self.pressed:
            screen.blit(self.hover_pic, self.screen_rect)
            self.label.draw(screen, dx=1, dy=1)
        elif self.hover:
            screen.blit(self.pressed_pic, self.screen_rect)
            self.label.draw(screen)
        else:
            screen.blit(self.normal_pic, self.screen_rect)
            self.label.draw(screen)
    

class LongLabelButton(LabelButton):
    def __init__(self, label, x=0, y=0, z=100):
        super().__init__(**self.get_res(res, "long_button"), label=label, x=x, y=y, z=z)

class NormalLabelButton(LabelButton):
    def __init__(self, label, x=0, y=0, z=100):
        super().__init__(**self.get_res(res, "button"), label=label, x=x, y=y, z=z)