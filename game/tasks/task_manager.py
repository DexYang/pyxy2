import os
import importlib
from utils.is_chinese import is_chinese


class TaskManager:
    _instance = None

    def __new__(cls):
        if not hasattr(cls, '_instance') or cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.TASKS = {}
        self.NPC = {}
        self.load()

    def touch(self, npc_name):
        if npc_name not in self.NPC:
            return False, False
        for task_name in self.NPC[npc_name].keys():
            task = self.TASKS[task_name]
            _type, _action = task.touch(npc_name)
            if _type == False:
                continue
            return _type, _action
        return False, False

    def load(self):
        abs_path = os.path.dirname(__file__) + "\\tasks"
        for item in os.listdir(abs_path):
            if os.path.isfile(os.path.join(abs_path, item)) and is_chinese(item[0]):
                name = 'game.tasks.tasks.' + item[:-3]
                importlib.import_module(name)
                module = importlib.find_loader(name).load_module(name)
                for attr_name in module.__dir__():
                    if attr_name.startswith("_") or attr_name == "TaskFlow":
                        continue
                    clz = getattr(module, attr_name)
                    task = clz()
                    for task_npc in task.NPC.keys():
                        if task_npc not in self.NPC:
                            self.NPC[task_npc] = {}
                        self.NPC[task_npc][task.name] = True
                    self.TASKS[task.name] = task


task_manager = TaskManager()
