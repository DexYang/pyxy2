class Context:
    def __init__(self):
        self.delta_time = 0.0
        self.current_time = 0.0

        self.left = 0
        self.top = 0

        self.loc_changed = False

        self.dirty_window = None

        self.mouse_x = 0
        self.mouse_y = 0

        self.events = []

    def set_events(self, events):
        self.events = events

    def get_events(self):
        return self.events

    def set_time(self, delta_time, current_time):
        self.delta_time = delta_time
        self.current_time = current_time

    def get_current_time(self):
        return self.current_time

    def set_left_top(self, left, top):
        if self.left == left and self.top == top:
            self.loc_changed = False
        else:
            self.loc_changed = True
            self.left = left
            self.top = top

    def get_left_top(self):
        return self.left, self.top

    def set_mouse_pos(self, pos):
        self.mouse_x, self.mouse_y = pos

    def get_mouse_pos(self):
        return self.mouse_x, self.mouse_y

    def set_dirty_window(self, dirty_window):
        self.dirty_window = dirty_window

    def get_dirty_window(self):
        return self.dirty_window
