import os
import pygame as pg
from pygame.locals import *
import pygame.freetype as freetype

from core.ui.node import Node
from lib import ptext

os.environ["SDL_IME_SHOW_UI"] = "1"


class Input(Node):
    def __init__(self, font_size=14, text_color=(255, 255, 255), no_chinese=False, x=0, y=0, w=0, h=16, z=0):
        super().__init__(None, x, y, w, h, z)

        self.font = freetype.SysFont("simsun", font_size)
        self.text_color = text_color
        self.font_size = font_size

        self._text = ""
        self.cursor = 0
        self.cursor_pixel_x = 0

        self.cursor_surface = pg.surface.Surface((1, self.h))
        self.cursor_surface.fill(self.text_color)

        self.surface = pg.surface.Surface((w, h), flags=pg.SRCALPHA)

        self.slide_window_left = 0

        self.last_time = 0
        self.blinkRate = 500
        self.show_blink = False
        self.hover = False

        self.no_chinese = no_chinese

        self.padding_top = max(0, (h - font_size) // 2)

        self.text_position = [0]

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        pos = 0
        self.text_position = [0]
        for char in self._text:
            pos += self.font_size if self.is_chinese(char) else self.font_size // 2
            self.text_position.append(pos)

    def update(self, context):
        if self.hidden:
            return
        self.screen_rect = self.rect.move(*self.get_parent_screen_xy())

        if self.focus:
            current = context.get_current_time()
            if current > self.last_time + self.blinkRate:
                self.show_blink = not self.show_blink
                self.last_time = current
            self.cursor_pixel_x = self.text_position[self.cursor]
            self.slide_window_left = max(0, self.cursor_pixel_x - self.w)


    def draw(self, screen):
        if self.hidden:
            return
        pg.draw.rect(screen, (255, 0, 0), self.screen_rect, width=2)
        if self.text:
            self.surface.fill((0, 0, 0, 0))
            ptext.draw( text=self.text, 
                        pos=(-self.slide_window_left, self.padding_top), 
                        surf=self.surface,
                        fontsize=self.font_size,
                        color=self.text_color, sysfontname="simsun")
            screen.blit(self.surface, self.screen_rect)
        if self.focus and self.show_blink:
            screen.blit(self.cursor_surface, (self.screen_rect.x + min(self.cursor_pixel_x, self.w), self.screen_rect.y))
    

    def on_key_down(self, event):
        if self.focus:
            key = event.key
            print(event, event.__dict__)
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
            elif key == K_END:
                self.cursor = len(self.text)
            elif key == K_HOME:
                self.cursor = 0
            elif key == K_KP_ENTER or key == K_RETURN:
                self.emit("text_enter", input_id=self.id, text=self.text)
            elif key == K_c and event.mod == 4160:
                print("CTRL  C")
            elif key == K_v and event.mod == 4160:
                _bytes = pg.scrap.get(pg.SCRAP_TEXT)[:-1]
                self.add_text(_bytes.decode("utf-8"))
            event.handled = True

    def on_text_input(self, event):
        if self.focus:
            self.add_text(event.text)
            event.handled = True

    def add_text(self, _text):
        text = "".join([c for c in _text if not self.no_chinese or not self.is_chinese(c)])
        self.text = self.text[:self.cursor] + text + self.text[self.cursor:]
        self.cursor += len(text)

    def on_mouse_left_down(self, event):
        if not event.processed and self.is_in(event.pos):
            relative_x = event.pos[0] - self.screen_rect.x
            select_x = min(self.text_position[-1], relative_x)
            index = -1
            for pos in self.text_position:
                if select_x < pos:
                    break
                index += 1
            self.cursor = index
            self.focus = True
            event.processed = True
            pg.key.set_text_input_rect(self.screen_rect)
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
