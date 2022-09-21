from core.animated.animated_sprite import AnimatedSprite
from res.characters import characters
from core.animated.character_state import CharacterStandNormalState, CharacterStandTeaseState, CharacterWalkingState, \
    CharacterRunningState


class Character(AnimatedSprite):
    INIT_STATE = "stand_normal"
    STATES_CLASS = {
        "stand_normal": CharacterStandNormalState,
        "stand_tease": CharacterStandTeaseState,
        "run": CharacterRunningState,
        "walk": CharacterWalkingState
    }

    def __init__(self, race, version, character_id, x=0, y=0):
        self.RES_INFO = characters[race][version][character_id]
        super().__init__(x, y)

        self.race = race
        self.version = version
        self.character_id = character_id

        self.target = (0, 0)
        self.target_list = []
        self.is_new_target = False
        self.is_running = False

        self.mask = None

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
