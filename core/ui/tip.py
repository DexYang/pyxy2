from core.ui.static_node import StaticNode
from core.ui.text import Text
import pygame
from pygame import Rect


class Tip(StaticNode):
    def __init__(self, text, x=0, y=0, z=0):
        super().__init__("gires.wdf", "0x8D580095", None, x, y, z)
        self.text = Text(text, w=280)
        self.add_child(self.text)

        self.horizon_mul = 14  # tip总长320
        self.vertical_mul = max(self.text.h // 20 + 1, 1)
        self.scale9(self.horizon_mul, self.vertical_mul)

        self.text.x = (320 - self.text.max_width) // 2 + 10
        self.text.y = 8 if self.text.first_line_emoji else 15

        self.start_time = 0
        self.just_init = True

        self.pressed = False
        self._x = 0
        self._y = 0

    def update(self, context):
        if self.just_init:
            self.start_time = context.get_current_time()
            self.just_init = False
        self.screen_rect = self.rect.move(*self.get_parent_screen_xy())
        self.update_children(context)
        if context.get_current_time() - self.start_time > 5000:
            self.useless = True

    def draw(self, screen):
        if self.hidden:
            return
        screen.blit(self.surface, self.screen_rect)
        self.draw_children(screen)
    
    def scale9(self, horizon_mul, vertical_mul):
        left_top = self.surface.subsurface(Rect((0, 0), (20, 20)))
        mid_top = self.surface.subsurface(Rect((20, 0), (20, 20)))
        right_top = self.surface.subsurface(Rect((40, 0), (20, 20)))

        left = self.surface.subsurface(Rect((0, 20 ), (20, 20)))
        mid = self.surface.subsurface(Rect((20, 20), (20, 20)))
        right = self.surface.subsurface(Rect((40, 20), (20, 20)))

        left_bottom = self.surface.subsurface(Rect((0, 40), (20, 20)))
        mid_bottom = self.surface.subsurface(Rect((20, 40), (20, 20)))
        right_bottom = self.surface.subsurface(Rect((40, 40), (20, 20)))

        w = 40 + 20 * horizon_mul
        h = 40 + 20 * vertical_mul
        temp_surface = pygame.Surface((w, h), pygame.SRCALPHA)

        for i in range(vertical_mul + 2):
            for j in range(horizon_mul + 2):
                if i == 0:  # 第一行
                    if j == 0:
                        temp_surface.blit(left_top, (20 * j, 20 * i))
                    elif j == horizon_mul + 1:
                        temp_surface.blit(right_top, (20 * j, 20 * i))
                    else:
                        temp_surface.blit(mid_top, (20 * j, 20 * i))
                elif i == vertical_mul + 1:
                    if j == 0:
                        temp_surface.blit(left_bottom, (20 * j, 20 * i))
                    elif j == horizon_mul + 1:
                        temp_surface.blit(right_bottom, (20 * j, 20 * i))
                    else:
                        temp_surface.blit(mid_bottom, (20 * j, 20 * i))
                else:
                    if j == 0:
                        temp_surface.blit(left, (20 * j, 20 * i))
                    elif j == horizon_mul + 1:
                        temp_surface.blit(right, (20 * j, 20 * i))
                    else:
                        temp_surface.blit(mid, (20 * j, 20 * i))
        self.surface = temp_surface
        self.h = (vertical_mul + 2) * 20
        self.w = (horizon_mul + 2) * 20
        self.rect.width = self.w
        self.rect.height = self.h

    def on_mouse_left_up(self, event):
        if self.screen_rect.collidepoint(*event.pos):
            self.useless = True
            self.pressed = False

    def on_mouse_left_down(self, event): 
        if self.screen_rect.collidepoint(*event.pos):
            self.pressed = True
            event.handled = True
            self._x = event.pos[0]
            self._y = event.pos[1]

    def on_mouse_right_up(self, event): 
        if self.screen_rect.collidepoint(*event.pos):
            self.useless = True
            self.pressed = False

    def on_mouse_motion(self, event): 
        if self.screen_rect.collidepoint(*event.pos):
            if self.pressed:
                delta_x = event.pos[0] - self._x
                delta_y = event.pos[1] - self._y
                self.rect.move_ip(delta_x, delta_y)
                self._x = event.pos[0]
                self._y = event.pos[1]
            event.processed = True