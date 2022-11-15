from core.animated.npc import NPC


class 长安桥驿站(NPC):
    X = 5212
    Y = 3958

    CHAR_ID = 3015

    def get_dialog_content(self):
        return {
            "title": "这里是长安清风桥，你想要去哪里呢？",
            "options": {
                "目的地1": lambda : self.emit("tip", text="目的地1"),
                "目的地2": lambda : self.emit("tip", text="目的地2")
            }
        }