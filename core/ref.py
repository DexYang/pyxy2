import uuid
from utils.logger import logger
from core.event_dispatcher import EVENT_DISPATCHER
from core.sound_manager import SOUND_MANAGER


class Ref:
    def __init__(self):
        self.event_dispatcher = EVENT_DISPATCHER
        self.id = uuid.uuid1()
        self.__register()
        self.log = logger
        self.sound = SOUND_MANAGER

    def notify(self, event_name, **kwargs):
        self.event_dispatcher.dispatch_event(event_name, **kwargs)

    def emit(self, event_name, **kwargs):
        self.event_dispatcher.post(event_name, **kwargs)

    def handle_event(self, event):
        if hasattr(self, "on_" + event.name):  # 如果self有该事件的处理方法
            getattr(self, "on_" + event.name)(event)  # 则处理

    def __register(self):
        self.__travel_handler(self.event_dispatcher.register_event)

    def __del__(self):
        self.__travel_handler(self.event_dispatcher.drop_event)

    def __travel_handler(self, callback):
        method_list = [func for func in dir(self) if func.startswith('on_') and callable(getattr(self, func))]
        for method_name in method_list:
            callback(method_name[3:], self)

    def destroy(self):
        self.__del__()

    def play(self, wdf, _hash, loop=False):
        self.sound.play(wdf, _hash, loop)

    def music(self, wdf, _hash):
        self.sound.music(wdf, _hash)
