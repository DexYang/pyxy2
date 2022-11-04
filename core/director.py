import random
import pygame as pg
from pygame.locals import USEREVENT

from core.context import Context
from core.ref import Ref
from core.event import INTERACTIVE_EVENTS, OTHER_EVENTS, Event

import time
from core.ui.node import Blank
from core.ui.tip import Tip
from core.ui.quit_dialog import QuitDialog
from core.role_manager import role_manager

from lib.pyxy2 import end_loop
from utils import transitions


class Director(Ref):
    def __init__(self, title="Director", resolution=(640, 480), fps=60):
        super().__init__()
        pg.init()
        self.title = title
        self.width, self.height = resolution

        self.fps = fps
        self.clock = pg.time.Clock()

        self.running = True
        self._screen = pg.display.set_mode(resolution)
        pg.display.set_icon(pg.image.load('ico.ico'))

        pg.key.set_repeat(150, 50)

        self.scene_class_pool = {}
        self._scene = None
        self._old_scene = None

        from core.mouse import Mouse
        pg.mouse.set_visible(False)
        self.mouse = Mouse(0, 0)

        self.tip_layer = Blank()

        self.tip_x = 0
        self.tip_y = 0
        self.tip_count = 0
        self.last_tip = 0
        self.reset_tip(resolution)

        self.quit_dialog = QuitDialog()
        self.quit_dialog.hidden = True

        self.time_passes = 0
        self.last_30s = 0
        self.last_60s = 0
        self.last_120s = 0
        
        self.transition = transitions
        self.transition_choices = ['fadeOutUp', 'fadeOutDown', 'fadeOut', 'fadeOut', 'fadeOut',
                                   'moveUp', 'moveDown', 'moveLeft', 'moveRight', 'moveUpLeft', 'moveUpRight']
        self.transition.init(self._screen, *self.resolution)

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
        if self._screen.get_size() != value:
            self._screen = pg.display.set_mode(value)
        self.reset_tip(value)

    def reset_tip(self, resolution):
        self.tip_x = resolution[0] // 2 - 150
        self.tip_y = resolution[1] // 2 - 50

    def handle_events(self, events):
        for event in events:
            event_attributes = event.__dict__
            print(event.type, event_attributes)
            if event.type in INTERACTIVE_EVENTS:
                event_type = INTERACTIVE_EVENTS[event.type]
                if isinstance(event_type, dict):  # 如果有二级列表
                    if event_attributes["button"] not in event_type:
                        continue
                    event_attributes["name"] = event_type[event_attributes["button"]]
                else:
                    event_attributes["name"] = event_type
                event = Event(event_attributes["name"], **event_attributes)
                
                self.tip_layer.handle_events(event)
                self._scene.handle_events(event)  # 交互事件按Z轴传递
            elif event.type in OTHER_EVENTS:
                event_attributes["name"] = OTHER_EVENTS[event.type]
                self.notify(event_name=event_attributes["name"], **event_attributes)
            elif event.type == USEREVENT:
                self.notify(event_name=event_attributes["name"], **event_attributes)

    def update(self, context):
        self.mouse.update(context)
        self.tip_layer.update(context)
        self._scene.update(context)

    def draw(self):
        # self._screen.fill((70, 70, 70))
        self._screen.fill((0, 0, 0))
        self._scene.draw(self._screen)
        self.tip_layer.draw(self._screen)
        self.mouse.draw(self._screen)

    def run(self, scene_class_name=None):
        if scene_class_name:
            self.change_scene(scene_class_name, "fadeOut")

        context = Context()
        while self.running:
            events = pg.event.get()

            context.set_mouse_pos(pg.mouse.get_pos())
            self.time_passes = pg.time.get_ticks()

            context.set_time(self.clock.tick(self.fps), self.time_passes)

            if self.time_passes - self.last_30s > 30000:
                self.last_30s = self.time_passes
                self.notify("every_30s")
            if self.time_passes - self.last_60s > 60000:
                self.last_60s = self.time_passes
                self.notify("every_60s")
            if self.time_passes - self.last_120s > 120000:
                self.last_120s = self.time_passes
                self.notify("every_120s")

            self.handle_events(events)

            self.update(context)

            self.draw()
            
            self.transition.update_screen()

            pg.display.update()

    def change_scene(self, scene_class_name, transition=None, *args, **kwargs):
        
        self.transition.init(self._screen, *self.resolution)
        if not transition:
            transition = random.choice(self.transition_choices)
        self.transition.run(transition, 0.7)
        
        scene = self.scene_class_pool[scene_class_name](*args, **kwargs)
        scene.enter()

        if self._scene:
            self._scene.exit()
            self._scene = None
        self._scene = scene
        self.mouse.change_state("normal")

    def on_change_scene(self, event):
        self.change_scene(scene_class_name=event.scene_name, **event.__dict__)
        event.handled = True

    def on_change_resolution(self, event): 
        self.resolution = event.resolution
        event.handled = True

    def init_scene(self, scene_pool):
        self.scene_class_pool = scene_pool

    def on_quit(self, event):
        self.quit_dialog.hidden = False
        self.quit_dialog.x = (self.resolution[0] - self.quit_dialog.w) // 2
        self.quit_dialog.y = (self.resolution[1] - self.quit_dialog.h) // 2

        self.tip_layer.add_child(self.quit_dialog)
        event.handled = True

    def on_exit(self, event): 
        self.running = False
        role_manager.logout()
        end_loop()
        event.handled = True

    def on_tip(self, event):
        if self.tip_count >= 5: 
            self.tip_count = 0
            self.reset_tip(self.resolution)
        ct = pg.time.get_ticks()
        if ct - self.last_tip > 8000: 
            self.tip_count = 0
            self.reset_tip(self.resolution)
        self.last_tip = ct
        self.tip_layer.add_child(Tip(event.text, self.tip_x, self.tip_y))
        self.tip_x += 20
        self.tip_y += 20
        self.tip_count += 1
        event.handled = True
