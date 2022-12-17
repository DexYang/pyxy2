from transitions import Machine
from core.role_manager import role_manager
from core.ref import Ref


class Flow(Ref):
    initial = "solid"

    states = ['solid', 'liquid', 'gas', 'plasma']

    transitions = [
        {'trigger': 'melt', 'source': 'solid', 'dest': 'liquid' },
        {'trigger': 'evaporate', 'source': 'liquid', 'dest': 'gas'},
        {'trigger': 'sublimate', 'source': 'solid', 'dest': 'gas'},
        {'trigger': 'ionize', 'source': 'gas', 'dest': 'plasma'}
    ]

    def __init__(self):
        super().__init__()
        
        self.machine = Machine(model=self, states=self.states, transitions=self.transitions, initial=self.initial)

    def proceed(self):
        pass


class Conversation(Flow):

    def conversations(self):
        return {
            "1": {
                "lines": "",
                "options": [
                    {
                        "label": "", "action": None
                    }
                ],
                "on_close": "2",
                "on_enter": None
            },
            "2": {
                "lines": "",
                "options": [
                    {
                        "label": "", "action": lambda : print("?????")
                    }
                ],
                "on_close": "1"
            }
        }

    # action|on_close   可以是函数，可以是字符串，如果是字符串代表下一个状态key

    def __init__(self, conversations=None):
        self.states = []
        self.transitions = []

        self._conversations = conversations if conversations else self.conversations()

        for state, conversation in self._conversations.items():
            self.states.append(state)

            if "on_close" in conversation and isinstance(conversation["on_close"], str):
                next_state = conversation["on_close"]
                transition = {
                    'trigger': state + "_" + next_state, 'source': state, 'dest': next_state
                }
                self.transitions.append(transition)
            
            for op in conversation["options"]:
                if isinstance(op["action"] , str):
                    next_state = op["action"]
                    transition = {
                        'trigger': state + "_" + next_state, 'source': state, 'dest': next_state
                    }
                    self.transitions.append(transition)

        self.initial = self.states[0]

        super().__init__()

    def get(self):
        return self._conversations[self.state]

    def proceed(self, op = -1):
        if op == -1:
            if "on_close" not in self._conversations[self.state]:
                return False
            attr = self._conversations[self.state]["on_close"]
        else:
            attr = self._conversations[self.state]["options"][op]["action"]
        if isinstance(attr, str):
            if attr in self._conversations:
                getattr(self, self.state + "_" + attr)()
                if "on_enter" in self._conversations[attr]:
                    self._conversations[attr]["on_enter"]()
                return True
        elif callable(attr):
            attr()
        return False


class TaskFlow(Flow):
    initial = "领取"
    first = "1"

    def __init__(self, flow=None):
        self.name = self.__class__.__name__

        self.states = []
        self.transitions = []
        self.NPC = {}

        self._flow = flow if flow else self.flow()
        
        for state, node in self._flow.items():
            self.states.append(state)

            self.NPC[node["NPC"]] = True

            if "next" in node:
                for next_state in node["next"]:
                    transition = {
                        'trigger': state + "_" + next_state, 'source': state, 'dest': next_state
                    }
                    self.transitions.append(transition)

        super().__init__()

    def flow(self):
        return {
            "0": {
                "NPC": "",
                "action": lambda : ("对话", Conversation({
                    "1": {
                        "lines": "",
                        "options": [
                            {
                                "label": "领取任务", "action": "receive"
                            }
                        ],
                        "on_close": self.set_state("1")
                    },
                })),
                "condition": lambda : True
            },
            "1": {
                "NPC": "",
                "action": "对话"
            }
        }

    def receive(self):
        task = self.new()
        task.set_state(self.first)
        main_role = role_manager.main_role
        main_role.add_task(task)

    def touch(self, npc_name):
        main_role = role_manager.main_role
        if self.name in main_role.tasks:
            task = main_role.tasks[self.name]
            return task.proceed(npc_name)
        else:
            return self.claim(npc_name)

    def claim(self, npc_name):
        task_node = self.match(npc_name, self.initial)
        if not task_node:
            return False, None
        return self.action(task_node)

    def set_state(self, state):
        self.machine.set_state(state)

    def proceed(self, npc_name):
        task_node = self.match(npc_name, self.state)
        if not task_node:
            return False, None
        return self.action(task_node)

    def match(self, npc_name, state):
        _flow = self._flow
        task_node = _flow[state]
        if task_node["NPC"] != npc_name:
            return False
        return task_node

    def new(self):
        return type(self)()

    def action(self, node):
        if 'condition' in node:
            condition = node['condition']
            if callable(condition):
                if not condition():
                    return False, None
            else:
                if not condition:
                    return False, None
        action = node["action"]
        if isinstance(action, str):
            if hasattr(self, self.state + "_" + action):
                getattr(self, self.state + "_" + action)()
                return True, None
            elif hasattr(self, action):
                return getattr(self, action)()
        elif callable(action):
            return action()
        return False, None
