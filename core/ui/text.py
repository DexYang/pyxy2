from typing import List

from core.ui.node import Node
from core.ui.animation_node import AnimationNode
from lib import ptext
import re
from settings import XY2PATH

pattern = re.compile(r'[0-9a-fA-F]{6}')       

TEMPLATES = {
    "#R": ["color", "red"],
    "#G": ["color", "green"],
    "#B": ["color", "cyan"],
    "#K": ["color", "black"],
    "#Y": ["color", "yellow"],
    "#W": ["color", "white"],
    
    "#pink": ["color", "pink"],
    "#gold": ["color", "goldenrod2"],
    "#grey": ["color", "grey"],
    "#brown": ["color", "brown"],
    "#purple": ["color", "purple"],
    "#orange": ["color", "orange"],

    "#d": ["mode", "bold"],
    "#b": ["mode", "blink"],
    "#i": ["mode", "italic"],
    "#u": ["mode", "underline"],
    "#n": ["mode", "reset"],
    "#r": ["mode", "enter"]
}

PREFIX = {
    "#": 1,
    "#p": 1, "#pi": 1, "#pin": 1,
    "#b": 1, "#br": 1, "#bro": 1, "#brow": 1,
    "#g": 1, "#go": 1, "#gol": 1, "#gr": 1, "#gre": 1,
    "#o": 1, "#or": 1, "#ora": 1, "#oran": 1, "#orang": 1,
    "#p": 1, "#pi": 1, "#pin": 1, "#pu": 1, "#pur": 1, "#purp": 1, "#purpl": 1
}

EMOTE_WDF = "gires.wdf"


class Text(Node):
    def __init__(self, text, x=0, y=0, w=0, h=0, z=0, fontname="font/simsun.ttc", font_size=14):
        super().__init__(text, x, y, w, h, z)

        self.text = text

        self.fontname = XY2PATH + fontname
        self.font_size = font_size

        self.line_space = 5
        self.max_width = 0
        self.rebuild(self.translate(self.text))
        self.first_line_emoji = False
        

    def translate(self, text: str) -> List:
        content = []
        i = 0
        pattern_matching = False
        last_pattern = None
        pattern_text_cache: str = "#"

        while i < len(text):
            s = text[i]
            if s == '#':
                if pattern_matching: 
                    if last_pattern:
                        content.append(self.pattern_transform(last_pattern))
                        last_pattern = None
                        pattern_text_cache = "#"
                    else:
                        content.append("#")
                pattern_matching = True
            elif s.isdigit():
                if pattern_matching:
                    pattern_text_cache += s
                    numbers = pattern_text_cache[1:]
                    if numbers.isdigit():  # #后面都是数字
                        if len(numbers) <= 2:
                            last_pattern = [EMOTE_WDF, "EMOTE/{:02d}.tca".format(int(numbers))]
                        else:
                            last_pattern = [EMOTE_WDF, "EMOTE/{:02d}.tca".format(int(numbers[:2]))]
                            content.append(self.pattern_transform(last_pattern))
                            for x in numbers[2:]:
                                content.append(x)
                            pattern_matching = False
                            last_pattern = None
                            pattern_text_cache = "#"
                else: 
                    content.append(text[i])
            elif s.isalpha() or s == '/':
                if pattern_matching:
                    pattern_text_cache += s
                    if pattern_text_cache in TEMPLATES:
                        last_pattern = TEMPLATES[pattern_text_cache]
                    if pattern_text_cache == "#c":
                        if pattern.match(text[i+1: i+7]): 
                            r = int(text[i+1: i+3], 16)
                            g = int(text[i+3: i+5], 16)
                            b = int(text[i+5: i+7], 16)
                            content.append(self.pattern_transform(["color", (r, g, b)]))
                            i += 6
                            pattern_matching = False
                            last_pattern = None
                            pattern_text_cache = "#"
                        else: 
                            for x in pattern_text_cache:
                                content.append(x)
                    if pattern_text_cache not in PREFIX:
                        if last_pattern:
                            content.append(self.pattern_transform(last_pattern))
                            if last_pattern[0] == EMOTE_WDF:
                                content.append(s)
                        else:
                            for x in pattern_text_cache:
                                content.append(x)
                        pattern_matching = False
                        last_pattern = None
                        pattern_text_cache = "#"
                else: 
                    content.append(text[i])
            else:
                if pattern_matching:
                    if last_pattern:
                        content.append(self.pattern_transform(last_pattern))
                    else:
                        for x in pattern_text_cache:
                            content.append(x)
                    pattern_matching = False  # 退出匹配模式
                    last_pattern = None
                    pattern_text_cache = "#"
                else: 
                    content.append(text[i])
            i += 1
        if last_pattern:
            content.append(self.pattern_transform(last_pattern))
        elif pattern_text_cache != "#":
            for x in pattern_text_cache:
                content.append(x)
        return content

    def get_text(self, x, y, text=None): 
        newText = TextWrapper(x = x, y = y, fontname=self.fontname, fontsize=self.font_size)
        if text:
            newText.color = text.color
            newText.bold = text.bold
            newText.italic = text.italic
            newText.blink = text.blink
            newText.underline = text.underline
        return newText

    def rebuild(self, content):
        x = 0
        y = 0
        text = self.get_text(x, y)
        line_height = self.font_size

        i = 0
        line_height_correcter = {0: line_height}

        for c in content: 
            if isinstance(c, EmojiWrapper): 
                if not text.is_empty():
                    text.line = i
                    self.add_child(text)
                if x + c.w > self.w + 5:  # 宽度不足，换行
                    self.max_width = max(self.max_width, x + c.w)
                    x = 0
                    i += 1
                    line_height_correcter[i] = c.h  # 新换行
                else:
                    x += 2
                c.x = x
                c.line = i
                x += c.w + 2
                line_height_correcter[i] = max(line_height_correcter[i], c.h)
                self.add_child(c)
                text = self.get_text(x, y, text)
            elif isinstance(c, ColorWrapper):
                if not text.is_empty():
                    text.line = i
                    self.add_child(text)
                    newText = self.get_text(x, y, text)
                    text = newText
                text.color = c.color
            elif isinstance(c, ModeWrapper): 
                if not text.is_empty():
                    text.line = i
                    self.add_child(text)
                    text = self.get_text(x, y, text)

                if c.mode == "bold": 
                    text.bold = True
                elif c.mode == "blink": 
                    text.blink = True
                elif c.mode == "italic": 
                    text.italic = True
                elif c.mode == "underline": 
                    text.underline = True
                elif c.mode == "reset": 
                    text.clean()
                elif c.mode == "enter": 
                    text.x = 0
                    self.max_width = max(self.max_width, x)
                    x = 0
                    i += 1
                    line_height_correcter[i] = 0
            else: 
                char_len = self.font_size if self.is_chinese(c) else self.font_size // 2
                if x + char_len > self.w:  # 宽度不足，换行
                    text.line = i
                    self.max_width = max(self.max_width, x + char_len)
                    self.add_child(text)
                    x = 0
                    i += 1
                    line_height_correcter[i] = self.font_size
                    text = self.get_text(x, y, text)
                x += char_len
                text.append(c)
                line_height_correcter[i] = max(line_height_correcter[i], self.font_size)
        
        if not text.is_empty():
            text.line = i
            self.add_child(text)
        self.max_width = max(self.max_width, x)

        y = 0
        for _i in range(i+1): 
            if _i == 0:
                self.first_line_emoji = line_height_correcter[_i] > self.font_size
            line_height = line_height_correcter[_i]
            line_height_correcter[_i] = (y, line_height)
            y += line_height + self.line_space
        for child in self.children.values():
            y, line_height = line_height_correcter[child.line]
            if isinstance(child, TextWrapper):
                child.y = y + line_height - self.font_size
            elif isinstance(child, EmojiWrapper): 
                child.y = y + line_height + 2
        self.h = y
            

    @staticmethod
    def pattern_transform(pattern):
        if pattern[0] == "color":
            return ColorWrapper(pattern[1])
        elif pattern[0] == EMOTE_WDF:
            return EmojiWrapper(pattern[1])
        elif pattern[0] == "mode":
            return ModeWrapper(pattern[1])

    def update(self, context):
        if self.hidden:
            return
        self.screen_rect = self.rect.move(*self.get_parent_screen_xy())
        self.update_children(context)

    def draw(self, screen):
        return self.draw_children(screen) 

    @staticmethod
    def is_chinese(uchar):
        if len(uchar) != 1:
            raise TypeError('expected a character, but a string found!')
        if u'\u4e00' <= uchar <= u'\u9fa5':
            return True
        else:
            return False


class ColorWrapper:
    def __init__(self, color):
        self.color = color

class EmojiWrapper(AnimationNode):
    animation_rate = 120

    def __init__(self, was_hash):
        super().__init__(EMOTE_WDF, was_hash)
        self.line = 0

class ModeWrapper:
    def __init__(self, mode):
        self.mode = mode

class TextWrapper(Node):
    AnimationRate = 50

    def __init__(self,  color="white", 
                        bold=False, 
                        italic=False,
                        blink=False,
                        underline=False,
                        fontname="",
                        fontsize=16,
                        x=0, y=0, w=0, h=0):
        super().__init__(x=x, y=y, w=w, h=h)
        self.text = ""
        self.len = 0
    
        self.color = color
        self.bold = bold
        self.italic = italic
        self.blink = blink
        self.underline = underline
        self.fontsize = fontsize
        self.fontname = fontname

        self.line = 0

        self.last_time = 0
        self.alpha = 1
        self.alpha_direction = 'down'
    
    def update(self, context):
        super().update(context)
        if self.blink:
            current_time = context.get_current_time()
            if current_time > self.last_time + self.AnimationRate:
                if self.alpha_direction == 'down':
                    self.alpha -= 0.1
                    if self.alpha <= 0: 
                        self.alpha = 0
                        self.alpha_direction = 'up'
                else: 
                    self.alpha += 0.1
                    if self.alpha >= 1: 
                        self.alpha = 1
                        self.alpha_direction = 'down'
                self.last_time = current_time

    @staticmethod
    def is_chinese(uchar):
        if len(uchar) != 1:
            raise TypeError('expected a character, but a string found!')
        if u'\u4e00' <= uchar <= u'\u9fa5':
            return True
        else:
            return False

    def append(self, char):
        self.text += char
        self.len += self.fontsize if self.is_chinese(char) else self.fontsize / 2

    def is_empty(self):
        return True if self.text == "" else False

    def clean(self):
        self.color = None
        self.bold = False
        self.italic = False
        self.blink = False
        self.underline = False

    def draw(self, screen):
        ptext.draw(self.text, pos=self.screen_rect.topleft, color=self.color, bold=self.bold, italic=self.italic, underline=self.underline, fontsize=self.fontsize, fontname=self.fontname, alpha=self.alpha)