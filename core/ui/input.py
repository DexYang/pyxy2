import os
import pygame as pg
from pygame.locals import *
import pygame.freetype as freetype

from core.ui.node import Node
from lib import ptext

from utils.is_chinese import is_chinese
import pyperclip

os.environ["SDL_IME_SHOW_UI"] = "1"


class Input(Node):
    def __init__(self, font_size=14, text_color=(255, 255, 255), no_chinese=False, x=0, y=0, w=0, h=16, z=0):
        super().__init__(None, x, y, w, h, z)

        self.font = freetype.SysFont("simsun", font_size)
        self.text_color = text_color
        self.font_size = font_size

        self._text = ""
        self._cursor = 0
        self.cursor_pixel_x = 0

        self.cursor_surface = pg.surface.Surface((1, self.h))
        self.cursor_surface.fill(self.text_color)

        self.surface = pg.surface.Surface((w, h), flags=pg.SRCALPHA)

        self.slide_window_left = 0

        self.last_time = 0
        self.blinkRate = 500
        self.show_blink = False
        self.hover = False
        self.pressed = False

        self.no_chinese = no_chinese

        self.padding_top = max(0, (h - font_size) // 2)

        self.text_position = [0]

        self.pressed_cursor = 0
        self.selected_cursor = 0

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        pos = 0
        self.text_position = [0]
        for char in self._text:
            pos += self.font_size if is_chinese(char) else self.font_size // 2
            self.text_position.append(pos)

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, cursor):
        self._cursor= cursor
        self.cursor_pixel_x = self.text_position[self._cursor]
        if self.cursor_pixel_x < self.slide_window_left:
            self.slide_window_left = self.cursor_pixel_x
        elif self.cursor_pixel_x > self.slide_window_left + self.w:
            self.slide_window_left = self.cursor_pixel_x - self.w

    def update(self, context):
        if self.hidden:
            return
        self.screen_rect = self.rect.move(*self.get_parent_screen_xy())

        if self.focus:
            current = context.get_current_time()
            if current > self.last_time + self.blinkRate:
                self.show_blink = not self.show_blink
                self.last_time = current

    def draw(self, screen):
        if self.hidden:
            return
        pg.draw.rect(screen, (255, 0, 0), self.screen_rect, width=2)
        if self.text:
            self.surface.fill((0, 0, 0, 0))
            if self.selected_cursor != self.pressed_cursor:
                left = self.text_position[min(self.selected_cursor, self.pressed_cursor)]
                right = self.text_position[min(max(self.selected_cursor, self.pressed_cursor), len(self.text_position) - 1)]
                select_rect = pg.Rect(left - self.slide_window_left, 0, right - left, self.h)
                pg.draw.rect(self.surface, (0, 160, 220, 170), select_rect)
            ptext.draw( text=self.text, 
                        pos=(-self.slide_window_left, self.padding_top), 
                        surf=self.surface,
                        fontsize=self.font_size,
                        color=self.text_color, sysfontname="simsun")
            screen.blit(self.surface, self.screen_rect)
        if self.focus and self.show_blink:
            screen.blit(self.cursor_surface, (self.screen_rect.x + self.cursor_pixel_x - self.slide_window_left, self.screen_rect.y))
    
    def on_key_down(self, event):
        try:
            if self.focus:
                key = event.key
                if key == pg.K_BACKSPACE:
                    if len(self.text) > 0 and self.cursor > 0:
                        if self.selected_cursor != self.pressed_cursor:
                            left = min(self.selected_cursor, self.pressed_cursor)
                            right = max(self.selected_cursor, self.pressed_cursor)
                            self.text = self.text[:left] + self.text[right:]
                            self.cursor = left
                            self.selected_cursor, self.pressed_cursor = 0, 0
                        else:
                            self.text = self.text[:self.cursor-1] + self.text[self.cursor:]
                            self.cursor = max(0, self.cursor - 1)
                elif key  == pg.K_DELETE:
                    if self.selected_cursor != self.pressed_cursor:
                        left = min(self.selected_cursor, self.pressed_cursor)
                        right = max(self.selected_cursor, self.pressed_cursor)
                        self.text = self.text[:left] + self.text[right:]
                        self.cursor = left
                        self.selected_cursor, self.pressed_cursor = 0, 0
                    else:
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
                elif event.mod == 4160 and (key == K_c or key == K_x):
                    left = min(self.selected_cursor, self.pressed_cursor)
                    right = max(self.selected_cursor, self.pressed_cursor)
                    pyperclip.copy(self.text[left:right])
                    if key == K_x:
                        self.text = self.text[:left] + self.text[right:]
                        self.cursor = left
                        self.selected_cursor, self.pressed_cursor = 0, 0
                elif key == K_v and event.mod == 4160:
                    s = pyperclip.paste()
                    self.add_text(s)
                event.handled = True
        except Exception as e:
            self.log.info(e)

    def on_text_input(self, event):
        if self.focus:
            self.add_text(event.text)
            event.handled = True

    def add_text(self, _text):
        text = "".join([c for c in _text if not self.no_chinese or not is_chinese(c)])
        self.text = self.text[:self.cursor] + text + self.text[self.cursor:]
        self.cursor += len(text)

    def get_cursor(self, pos):
        relative_x = pos[0] - self.screen_rect.x + self.slide_window_left
        select_x = min(self.text_position[-1], relative_x)
        index = -1
        for pos in self.text_position:
            if select_x < pos:
                break
            index += 1
        return max(index, 0)

    def on_mouse_left_down(self, event):
        if not event.processed and self.is_in(event.pos):
            self.cursor = self.get_cursor(event.pos)

            self.pressed_cursor = self.cursor
            self.selected_cursor = self.cursor

            self.focus = True
            self.pressed = True
            event.processed = True
            pg.key.set_text_input_rect(self.screen_rect)
        else:
            self.focus = False

    def on_mouse_left_up(self, event):
        self.pressed = False

    def on_mouse_motion(self, event):
        if self.pressed:
            self.selected_cursor = self.get_cursor(event.pos)
            self.cursor = self.selected_cursor
            if event.pos[0] - self.screen_rect.x < 0:
                self.cursor = max(0, self.cursor - 1)
            elif event.pos[0] > self.screen_rect.x + self.w:
                self.cursor = min(len(self.text), self.cursor + 1)
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
