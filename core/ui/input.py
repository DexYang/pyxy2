import os
import pygame as pg
from pygame.locals import *
import pygame.freetype as freetype

from core.ui.node import Node
from lib import ptext

os.environ["SDL_IME_SHOW_UI"] = "1"
REPEAT = {
    K_BACKSPACE,
    K_DELETE,
    K_LEFT,
    K_RIGHT
}

class Input(Node):
    def __init__(self, font_size=14, text_color=(255, 255, 255), no_chinese=False, x=0, y=0, w=0, h=16, z=0):
        super().__init__(None, x, y, w, h, z)

        self.font = freetype.SysFont("simsun", font_size)
        self.text_color = text_color
        self.font_size = font_size

        self.text = ""
        self.cursor = 0
        self.cursor_pixel_len = 0

        self.cursor_surface = pg.surface.Surface((1, self.h))
        self.cursor_surface.fill(self.text_color)

        self.surface = pg.surface.Surface((w, h), flags=pg.SRCALPHA)

        self.slide_window_left = 0

        self.key_repeat_counter = {}
        self.frame_count = 0

        self.last_time = 0
        self.blinkRate = 500
        self.show_blink = False
        self.hover = False

        self.no_chinese = no_chinese

    def update(self, context):
        if self.hidden:
            return
        self.screen_rect = self.rect.move(*self.get_parent_screen_xy())

        if self.focus:
            current = context.get_current_time()
            if current > self.last_time + self.blinkRate:
                self.show_blink = not self.show_blink
                self.last_time = current

            if self.cursor != 0:
                tsurf, _ = ptext.draw(text=self.text[:self.cursor], pos=(0, 0), surf=self.surface, sysfontname="simsun", fontsize=self.font_size)
                self.cursor_pixel_len = tsurf.get_rect().w
            else:
                self.cursor_pixel_len = 0
            self.slide_window_left = max(0, self.cursor_pixel_len - self.w)

            self.frame_count += 1
            if self.frame_count > 5:
                self.frame_count = 0
                for key in self.key_repeat_counter.keys():
                    if key == pg.K_BACKSPACE:
                        if len(self.text) > 0 and self.cursor > 0:
                            self.text = self.text[:self.cursor-1] + self.text[self.cursor:]
                            self.cursor = max(0, self.cursor - 1)                       
                    elif key  == pg.K_DELETE:
                        self.text = self.text[:self.cursor] + self.text[self.cursor+1:]
                    elif key == pg.K_LEFT:
                        self.cursor = max(0, self.cursor - 1)
                    elif key == pg.K_RIGHT:
                        self.cursor = min(len(self.text), self.cursor + 1)

    def draw(self, screen):
        if self.hidden:
            return
        pg.draw.rect(screen, (255, 0, 0), self.screen_rect, width=2)
        if self.text:
            self.surface.fill((0, 0, 0, 0))
            ptext.draw( text=self.text, 
                        pos=(-self.slide_window_left, 0), 
                        surf=self.surface,
                        fontsize=self.font_size,
                        color=self.text_color, sysfontname="simsun")
            screen.blit(self.surface, self.screen_rect)
        if self.focus and self.show_blink:
            screen.blit(self.cursor_surface, (self.screen_rect.x + min(self.cursor_pixel_len, self.w), self.screen_rect.y))
        
    def on_key_up(self, event):
        if self.focus:
            key = event.key
            if key in REPEAT and key in self.key_repeat_counter:
                self.key_repeat_counter.pop(key)

    def on_key_down(self, event):
        if self.focus:
            key = event.key
            if key in REPEAT:
                self.key_repeat_counter[key] = True
                self.frame_count = 5
            elif key == K_END:
                self.cursor = len(self.text)
            elif key == K_HOME:
                self.cursor = 0
            elif key == K_KP_ENTER or key == K_RETURN:
                self.emit("text_enter", input_id=self.id, text=self.text)
            event.handled = True

    def on_text_input(self, event):
        if self.focus:
            text = "".join([c for c in event.text if not self.no_chinese or not self.is_chinese(c)])
            self.text = self.text[:self.cursor] + text + self.text[self.cursor:]
            self.cursor += len(text)
            event.handled = True

    def on_mouse_left_down(self, event):
        if not event.processed and self.is_in(event.pos):
            self.focus = True
            event.processed = True
        else:
            self.focus = False

    def on_mouse_motion(self, event):
        if not event.processed and self.is_in(event.pos):
            self.hover = True
            event.processed = True
            self.emit("change_mouse_state", state_name = "input")
            return
        if self.hover:
            self.emit("change_mouse_state", state_name = "normal")
        self.hover = False

    def get(self):
        return self.text

    @staticmethod
    def is_chinese(uchar):
        if len(uchar) != 1:
            raise TypeError('expected a character, but a string found!')
        if u'\u4e00' <= uchar <= u'\u9fa5':
            return True
        else:
            return False
