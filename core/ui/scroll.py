from core.ui.node import Node


class Scroll(Node):
    def __init__(self, line_space=4, x=0, y=0, w=0, h=0, z=0):
        super().__init__(None, x, y, w, h, z)
        self.line_space = line_space

        self.index = 0
        self.hover = False

        self.top = 0
        self.bottom = 0

    def add_child(self, node):
        if isinstance(node, Node):
            if node.name not in self.children:
                node.parent = self
                node.deep = self.deep + 1
                self.children[self.index] = node
                self.index += 1

    def handle_events(self, event):
        if self.hidden:
            return
        for i in range(self.top, self.bottom):
            self.children[i].handle_events(event)
            if event.handled:
                return
        return self.handle_event(event)

    def update(self, context):
        if self.hidden:
            return
        self.screen_rect = self.rect.move(*self.get_parent_screen_xy())
        i = self.top
        y = 0
        while True:
            if y > self.h:
                break
            if i in self.children:
                node = self.children[i]
                node.y = y
                node.update(context)
                y += node.h + self.line_space
            else:
                break
            i += 1
        self.bottom = i

    def draw(self, screen):
        if self.hidden:
            return
        for i in range(self.top, self.bottom):
            self.children[i].draw(screen)

    def on_mouse_wheel_up(self, event):
        if self.is_in(event.pos):
            self.top = max(self.top - 1, 0)
            self.emit("change_mouse_state", state_name="normal")
            event.handled = True

    def on_mouse_wheel_down(self, event):
        if self.is_in(event.pos):
            self.top = min(self.top + 1, self.index - 1)
            self.emit("change_mouse_state", state_name="normal")
            event.handled = True
