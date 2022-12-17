from core.animated.animated_sprite import AnimatedSprite
from data.character import characters
from core.animated.character_state import CharacterStandNormalState, CharacterStandTeaseState, CharacterWalkingState, \
    CharacterRunningState
from core.ui.text import Text


class Character(AnimatedSprite):
    INIT_STATE = "stand"
    STATES_CLASS = {
        "stand": CharacterStandNormalState,
        "stand2": CharacterStandTeaseState,
        "run": CharacterRunningState,
        "walk": CharacterWalkingState
    }

    WDF = "shape.wdf"
    WAS = "char/{:04d}/{}.tcp"

    def __init__(self, char_id: int, data: dict, x=0, y=0):
        self.char_id = char_id
        self.character = characters[char_id]
        
        self.data = data

        super().__init__(x, y)

        self.target = (0, 0)
        self.target_list = []
        self.is_new_target = False
        self.is_running = False

        self.mask = None

        self.set_name(self.data["称谓"][self.data["已选称谓"]], self.data["名字"])

        self.tasks = {}
    
    @property
    def x(self):  # x y为世界坐标，因为ani在draw时，已经减去锚点，实际上xy是人物锚点（人物脚底）
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

    @x.setter
    def x(self, x):
        self.rect.x = x
        self.data["x"] = x

    @y.setter
    def y(self, y):
        self.rect.y = y
        self.data["y"] = y

    def get_res(self, state_name, state_type):
        if state_type == "normal":
            return self.WDF, self.WAS.format(self.char_id, str(state_name))
        elif state_type == "武器":
            weapen_id = self.character["武器"][self.武器]
            return self.WDF, self.WAS.format(str(weapen_id), str(state_name))

    def reset_target(self):
        self.target = self.x, self.y

    def set_new_target(self, path_list, running):
        self.is_running = running
        self.target_list = path_list
        self.is_new_target = True

    def on_mouse_motion(self, event):
        if not event.processed:
            if self.get_at(*event.pos):
                self.hover = True
                event.processed = True
                return
        self.hover = False

    def get_at(self, x, y):
        return self.get_ani_screen_rect().collidepoint(x, y)

    def add_task(self, task):
        self.tasks[task.name] = task

    def set_name(self, nomination, name):
        y = 20
        # if nomination:
        #     if hasattr(self, "称谓"):
        #         self.称谓.set_text(nomination)
        #     else:
        #         self.称谓 = Text("#B#d"+nomination, w=100, h=16, font_size=16, shadow=True, font_name='font/AdobeSong.ttf')
        #         self.add_child(self.称谓)
        #     self.称谓.x = - self.称谓.max_width / 2
        #     self.称谓.y = y
        #     y += 20
        if hasattr(self, "名字"):
            self.名字.set_text(name)
        else:
            self.名字 = Text("#c00FF00#d"+name, w=100, h=16, font_size=16, shadow=True, font_name='font/AdobeSong.ttf')
            self.add_child(self.名字, override=True)
        self.名字.x = - self.名字.max_width / 2
        self.名字.y = y
        
