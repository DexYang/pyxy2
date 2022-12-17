from game.scenes.world_npc import WorldNPC
from core.flow import Conversation


class _对话(Conversation):
    def conversations(self):
        return {
            "1": {
                "lines": "这里是长安清风桥，你想要去哪里呢？",
                "options": [
                    {
                        "label": "长安桥", "action": lambda : self.notify("portal_world", tmap_name="老长安", tx=5000, ty=3900)
                    },
                    {
                        "label": "长安东", "action": lambda : self.notify("portal_world", tmap_name="长安东", tx=6020, ty=1630)
                    }
                ]
            }
        }



class 渔夫(WorldNPC):
    X = 433
    Y = 1858

    CHAR_ID = 3165

    conversation_class = _对话