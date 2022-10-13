from core.ui.button import Button
from core.ui.text import Text


class TextButton(Button):
    def __init__(self, text, fontname="", normal="#G", hover="#Y", font_size=14, value=None, x=0, y=0, z=100):
        self.value = value

        self.hover = False
        self.pressed = False

        self.text = Text(normal+text, w=800, h=font_size, font_size=font_size, fontname=fontname)
        super(Button, self).__init__(text, x, y, w=self.text.max_width, h=font_size, z=z)
        
        self.pressed_text = Text(hover+text, w=800, h=font_size, font_size=font_size, fontname=fontname)
        self.add_child(self.text)
        self.add_child(self.pressed_text)
        
    def update(self, context): 
        if self.hidden:
            return
        self.screen_rect = self.rect.move(*self.get_parent_screen_xy())
        if self.pressed:
            self.screen_rect.move_ip(1, 1)
        self.update_children(context)
            
    def draw(self, screen):
        if self.pressed or self.hover:
            self.pressed_text.draw(screen)
        else:
            self.text.draw(screen)
