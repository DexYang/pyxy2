import pygame as pg
from pygame.locals import USEREVENT

from core.context import Context
from core.ref import Ref
from core.event import INTERACTIVE_EVENTS, OTHER_EVENTS, Event
from lib.pyxy2 import end_loop
import time
from pygame.sprite import Sprite


class Director(Ref):
    def __init__(self, title="Director", resolution=(800, 600), fps=60):
        super().__init__()
        pg.init()
        self.title = title
        self.width, self.height = resolution

        self.fps = fps
        self.clock = pg.time.Clock()
        self.loops = 0
        self.loops_end = 20

        self.running = True
        self._screen = pg.display.set_mode(resolution)

        self.scene_class_pool = {}
        self._scene = None
        self._old_scene = None

    @property
    def title(self):
        return pg.display.get_caption()

    @title.setter
    def title(self, value):
        pg.display.set_caption(value)

    @property
    def resolution(self):
        return self._screen.get_size() if self._screen else (self.width, self.height)

    @resolution.setter
    def resolution(self, value):
        self.width, self.height = value
        self._screen = pg.display.set_mode(value)

    def handle_events(self):
        for event in pg.event.get():
            event_attributes = event.__dict__
            if event.type in INTERACTIVE_EVENTS:
                event_type = INTERACTIVE_EVENTS[event.type]
                if isinstance(event_type, dict):  # 如果有二级列表
                    if event_attributes["button"] not in event_type:
                        continue
                    event_attributes["name"] = event_type[event_attributes["button"]]
                else:
                    event_attributes["name"] = event_type
                event = Event(event_attributes["name"], **event_attributes)
                self._scene.handle_events(event)  # 交互事件按Z轴传递
            elif event.type in OTHER_EVENTS:
                event_attributes["name"] = OTHER_EVENTS[event.type]
                self.notify(event_name=event_attributes["name"], **event_attributes)
            elif event.type == USEREVENT:
                self.notify(event_name=event_attributes["name"], **event_attributes)

    def update(self, context):
        self._scene.update(context)

    def draw(self):
        self._screen.fill((70, 70, 70))
        self._scene.draw(self._screen)

    def run(self, scene_class_name=None):
        if scene_class_name:
            self.change_scene(scene_class_name)

        context = Context()
        while self.running:
            self.loops = self.loops + 1 if self.loops < self.loops_end else 0
            context.set_time(self.clock.tick(self.fps), pg.time.get_ticks(), self.loops)

            self.handle_events()

            self.update(context)

            self.draw()

            pg.display.update()

    def change_scene(self, scene_class_name):
        scene = self.scene_class_pool[scene_class_name]()
        scene.enter()

        if self._scene:
            self._scene.exit()
            self._scene = None
        self._scene = scene

    def init_scene(self, scene_pool):
        self.scene_class_pool = scene_pool

    def on_quit(self, event):
        self.running = False
        end_loop()
        event.handled = True
