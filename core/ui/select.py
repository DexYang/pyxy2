from core.ui.text_button import TextButton
from core.ui.node import Node


class Select(Node):
    def __init__(self, options, x=0, y=0):
        super().__init__(name=None, x=x, y=y)

        _y = 0

        def click(this):
            this.parent.select(this.value)

        i = 0
        for op in options:
            text_button = TextButton(op["label"], y = _y, value=i)
            text_button.click = text_button.method(click)
            self.add_child(text_button)
            _y += text_button.text.h + 5
            i += 1

    def select(self, value):
        self.parent.select(value)

    def update(self, context):
        if self.hidden:
            return
        self.screen_rect = self.rect.move(*self.get_parent_screen_xy())
        self.update_children(context)

    def draw(self, screen):
        if self.hidden:
            return
        import pygame as pg
        pg.draw.rect(screen, (255, 0, 0), self.screen_rect, 2)
        self.draw_children(screen)
