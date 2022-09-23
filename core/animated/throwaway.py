from core.animated.animated_sprite import AnimatedSprite


class Throwaway(AnimatedSprite):
    def __init__(self, wdf, was, x = 0, y = 0):
        self.WDF = wdf
        self.WAS = was
        super().__init__(x, y)

    def update(self, context):
        if self.state.update(context):
            self.useless = True
        left, top = context.get_left_top()
        self.screen_rect = self.rect.move(-left, -top)
        self.z = self.rect.y

    def refresh(self, x, y):
        self.useless = False
        self.x = x
        self.y = y
