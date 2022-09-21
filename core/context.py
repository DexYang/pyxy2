"""
update context
"""


class Context:
    def __init__(self):
        self.delta_time = 0.0
        self.current_time = 0.0
        self.loops = 0

        self.left = 0
        self.top = 0

        self.loc_changed = False

        self.dirty_window = None

    def set_time(self, delta_time, current_time, loops):
        self.delta_time = delta_time
        self.current_time = current_time
        self.loops = loops

    def is_restart_loops(self):
        return self.loops == 0

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

    def set_dirty_window(self, dirty_window):
        self.dirty_window = dirty_window

    def get_dirty_window(self):
        return self.dirty_window
