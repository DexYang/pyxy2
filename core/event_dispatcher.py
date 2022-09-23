import weakref
import pygame
from pygame.locals import USEREVENT
from core.event import Event


class EventDispatcher:
    _instance = None

    def __new__(cls):
        if not hasattr(cls, '_instance') or cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.EVENTS = {}
        self.pygame_post = pygame.event.post
        self.pygame_event = pygame.event.Event

    def register_event(self, event_name, obj):
        if event_name not in self.EVENTS:
            self.EVENTS[event_name] = {}
        self.EVENTS[event_name][obj.id] = weakref.ref(obj)

    def drop_event(self, event_name, obj):
        if event_name in self.EVENTS:
            if obj.id in self.EVENTS[event_name]:
                self.EVENTS[event_name].pop(obj.id)
            if len(self.EVENTS[event_name]) <= 0:
                self.EVENTS.pop(event_name)

    def dispatch_event(self, event_name, **kwargs):
        event = Event(event_name, **kwargs)
        if event_name in self.EVENTS:
            aimed_obj_dict = self.EVENTS[event_name]
            if "target_id" in kwargs:
                if kwargs["target_id"] in aimed_obj_dict:
                    aimed_obj_dict[kwargs["target_id"]]().handle_event(event)
            else:
                for ob_ref in aimed_obj_dict.values():
                    ob_ref().handle_event(event)
                    if event.handled:
                        break

    def post(self, event_name, **kwargs):
        self.pygame_post(self.pygame_event(USEREVENT, name=event_name, **kwargs))


EVENT_DISPATCHER = EventDispatcher()
