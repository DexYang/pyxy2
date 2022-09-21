from pygame import Vector2
from core.animated.animated_state import AnimatedState
from settings import WalkingSpeed, RunningSpeed


class CharacterState(AnimatedState):
    with_mask = True

    def is_moving_to_new_target(self):
        if self.parent.is_new_target:  # 有新的移动目的地
            if self.parent.is_running:
                self.change_state("run")
            else:
                self.change_state("walk")
            self.parent.is_new_target = False
            self.parent.reset_target()
            return True
        return False

    def is_on_target(self):
        return abs(self.parent.target[0] - self.parent.x) < 5 and \
               abs(self.parent.target[1] - self.parent.y) < 5


class CharacterMovingState(CharacterState):
    speed = 5

    def update(self, context):
        if self.is_moving_to_new_target():
            return
        if len(self.parent.target_list) > 0:
            if self.is_on_target():
                self.parent.target = self.parent.target_list.pop(0)
            self.move()
            super().update(context)
        elif self.is_on_target():
            self.change_state("stand_normal")
        else:
            self.move()
            super().update(context)

    def move(self):
        x = self.parent.x
        y = self.parent.y
        self.parent.direction = self.calc_direction(x, y)
        vector = Vector2()
        vector.x = self.parent.target[0] - x
        vector.y = self.parent.target[1] - y
        if vector.length() == 0:
            return
        vector.normalize_ip()
        vector.scale_to_length(self.speed)
        self.parent.x += vector.x
        self.parent.y += vector.y

    def calc_direction(self, _x, _y):
        x = self.parent.target[0] - _x
        y = self.parent.target[1] - _y
        if x == 0:
            if y < 0:
                return 6
            else:
                return 4
        y = y * 4096 / abs(x)
        if x > 0:
            if y < -9889:
                return 6
            if y < -1697:
                return 3
            if y < 1697:
                return 7
            if y < 9889:
                return 0
            return 4
        if y < -9889:
            return 6
        if y < -1697:
            return 2
        if y < 1697:
            return 5
        if y < 9889:
            return 1
        return 4


class CharacterWalkingState(CharacterMovingState):
    speed = WalkingSpeed
    res_index = "walk"


class CharacterRunningState(CharacterMovingState):
    speed = RunningSpeed
    res_index = "run"


class CharacterStandNormalState(CharacterState):
    res_index = "stand_normal"
    other_res = "stand_tease"
    loops = 5

    def __init__(self, wdf_name, was_hash):
        super().__init__(wdf_name, was_hash)
        self.loops_count = 0

    def update(self, context):
        if self.is_moving_to_new_target():
            return
        one_loop = super().update(context)
        if one_loop:
            self.loops_count += 1
            if self.loops_count >= self.loops:
                self.change_state(self.other_res)
                self.loops_count = 0


class CharacterStandTeaseState(CharacterStandNormalState):
    res_index = "stand_tease"
    other_res = "stand_normal"
    loops = 1
