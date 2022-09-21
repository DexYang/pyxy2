import pygame as pg
from settings import AnimationRate


class Animation:
    bright = pg.Surface((400, 400), flags=pg.SRCALPHA)
    bright.fill((80, 80, 80, 0))

    def __init__(self, was):
        self.direction_num = was.direction_num
        self.frame_num = was.frame_num
        self.key_x = was.x
        self.key_y = was.y
        self.width = was.width
        self.height = was.height
        self.time_seq = was.time

        self.frame_seq = []
        if self.time_seq and len(self.time_seq) > 0:
            count = 0
            for index, value in enumerate(self.time_seq):
                count = count + value
                while value >= 1:
                    self.frame_seq.append(index)
                    value -= 1
            self.frame_num = count
        else:
            self.frame_seq = [i for i in range(self.frame_num)]

        self.frames = []
        for i in range(len(was.frames)):
            self.frames.append([])
            for j in range(len(was.frames[i])):
                self.frames[i].append(Frame(was.frames[i][j]))

        self.frame = 0

        self.first_frame = 0
        self.last_frame = self.frame_num
        self.old_frame = 0

        self.last_time = 0

        self.is_forward = True

        self.direction = 0

    def update(self, current_time):
        one_loop = False
        if current_time > self.last_time + AnimationRate:
            self.frame += 1
            if self.frame >= self.last_frame:
                self.frame = self.first_frame
                one_loop = True  # 一次动画循环完毕
            self.last_time = current_time
        return one_loop

    def get_current_frame(self):
        return self.frames[self.direction][self.frame_seq[self.frame]]

    def set_direction(self, direction):
        self.direction = direction

    def draw(self, screen, x, y):
        frame = self.get_current_frame()
        surface = frame.surface.copy()
        screen.blit(surface, (x - frame.key_x, y - frame.key_y))


class Frame:
    def __init__(self, raw_frame):
        self.key_x = raw_frame["x"]
        self.key_y = raw_frame["y"]
        self.width = raw_frame["width"]
        self.height = raw_frame["height"]
        self.surface = pg.image.frombuffer(raw_frame["data"], (self.width, self.height), "RGBA").convert_alpha()
