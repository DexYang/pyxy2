from game.scenes.world_npc import WorldNPC
from core.flow import Conversation


class _对话(Conversation):
    def conversations(self):
        return {
            "1": {
                "lines": "这里是长安清风桥，你想要去哪里呢？",
                "options": [
                    {
                        "label": "目的地1", "action": "2"
                    },
                    {
                        "label": "目的地2", "action": lambda : self.emit("tip", text="目的地2")
                    }
                ]
            },
            "2": {
                "lines": "这里还是长安清风桥，你想要去哪里呢？",
                "options": [
                    {
                        "label": "目的地1", "action": "1"
                    },
                    {
                        "label": "目的地2", "action": lambda : self.emit("tip", text="目的地2")
                    }
                ]
            }
        }



class 测试NPC(WorldNPC):
    X = 5100
    Y = 3958

    CHAR_ID = 3011

    TOUCH_TASK = True

    conversation_class = _对话