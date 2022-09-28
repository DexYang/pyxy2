import pygame
from pygame.locals import *


class Event:
    def __init__(self, event_name, **kwargs):
        self.handled = False
        self.processed = False
        self.name = event_name
        for key, value in kwargs.items():
            self.__setattr__(key, value)


INTERACTIVE_EVENTS = {
    KEYDOWN: "key_down",
    KEYUP: "key_up",
    MOUSEBUTTONDOWN: {
        1: "mouse_left_down",  # MOUSE BUTTON DOWN = 5
        2: "mouse_mid_down",
        3: "mouse_right_down",
        4: "mouse_wheel_forward_down",
        5: "mouse_wheel_backward_down"
    },
    MOUSEBUTTONUP: {
        1: "mouse_left_up",  # MOUSE BUTTON UP = 6
        2: "mouse_mid_up",
        3: "mouse_right_up",
    },
    MOUSEMOTION: "mouse_motion"
}

OTHER_EVENTS = {
    QUIT: "quit"
}
