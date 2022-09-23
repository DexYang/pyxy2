from core.animated.animated_sprite import AnimatedSprite
from data.character import characters
from core.animated.character_state import CharacterStandNormalState, CharacterStandTeaseState, CharacterWalkingState, \
    CharacterRunningState


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

    def __init__(self, char_id: int, x=0, y=0):
        self.char_id = char_id
        self.character = characters[char_id]
        super().__init__(x, y)
        
        self.角色名 = self.character["角色名"]
        self.种族 = self.character["种族"]
        self.性别 = self.character["性别"]
        self.门派 = self.character["门派"]

        self.武器 = list(self.character["武器"].keys())[0]

        self.target = (0, 0)
        self.target_list = []
        self.is_new_target = False
        self.is_running = False

        self.mask = None

    def get_res(self, state_name, state_type):
        if state_type == "normal":
            return self.WDF, self.WAS.format(self.char_id, str(state_name))
        elif state_type == "武器":
            weapen_id = self.character["武器"][self.武器]
            return self.WDF, self.WAS.format(str(weapen_id), str(state_name))

    def update(self, context):
        self.state.update(context)
        left, top = context.get_left_top()
        self.screen_rect = self.rect.move(-left, -top)
        self.z = self.y

    def reset_target(self):
        self.target = self.x, self.y

    def set_new_target(self, path_list, running):
        self.is_running = running
        self.target_list = path_list
        self.is_new_target = True

    def on_mouse_motion(self, event):
        mouse_x, mouse_y = event.pos
        color = self.get_at(mouse_x, mouse_y)
        if color and color[3] > 0:
            self.hover = True
            print(self.hover)
            event.handled = True
        else:
            self.hover = False

    def get_at(self, x, y):
        ani_screen_rect = self.get_ani_screen_rect()
        if ani_screen_rect.collidepoint(x, y):
            return self.state.ani.get_at(x - ani_screen_rect.x, y - ani_screen_rect.y)
        return False