from core.flow import TaskFlow, Conversation as _Conversation


class 测试任务(TaskFlow):
    def flow(self):
        return {
            "领取": {
                "NPC": "老长安-测试NPC",
                "action": lambda : ("对话", _Conversation({
                    "1": {
                        "lines": "",
                        "options": [
                            {
                                "label": "领取任务", "action": lambda : self.receive()
                            }
                        ]
                    },
                })),
                "condition": lambda : True
            },
            "1": {
                "NPC": "老长安-测试NPC",
                "action": lambda : ("对话", _Conversation({
                    "1": {
                        "lines": "",
                        "options": [
                            {
                                "label": "领取任务@@@", "action": lambda : self.emit("tip", text="#Y????")
                            }
                        ]
                    },
                })),
            }
        }