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

        self.名字 = Text("#c00FF00#d"+self.data["名字"], w=100, h=16, font_size=16, shadow=True, font_name='font/AdobeSong.ttf')
        self.名字.x = - self.名字.max_width / 2
        self.名字.y = 20
        self.add_child(self.名字)
    
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
            if self.get_ani_screen_rect().collidepoint(*event.pos): 
                color = self.get_at(*event.pos)
                if color and color[3] > 0:
                    self.hover = True
                    event.processed = True
                    return
        self.hover = False

    def get_at(self, x, y):
        ani_screen_rect = self.get_ani_screen_rect()
        if ani_screen_rect.collidepoint(x, y):
            return self.state.ani.get_at(x - ani_screen_rect.x, y - ani_screen_rect.y)
        return False
        