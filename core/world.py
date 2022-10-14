import math
import os

import pygame as pg
from pygame.locals import Rect
from pygame.math import Vector2

from core.sprite import Sprite
from core.mask import Mask
from core.role_manager import role_manager
from core.animated.character import Character
from core.animated.throwaway import Throwaway

from lib.map import Map

from settings import WindowSize, XY2PATH


class World(Sprite):
    def __init__(self, map_id, left=0, top=0):
        super().__init__()

        self.map_id = map_id  # scene/1001.map
        
        if os.path.exists(XY2PATH + 'scene/' + str(map_id) + '.map'):
            self.map_version = 'scene'
        elif os.path.exists(XY2PATH + 'newscene/' + str(map_id) + '.map'):
            self.map_version = 'newscene'
        self.map_path = XY2PATH + self.map_version + '/' + str(map_id) + '.map'

        self.map = Map(self.map_path)
        self.rect = Rect((0, 0), (self.map.width, self.map.height))  # 整个地图范围

        self.map_block_info = {}
        i = 0
        for row in range(self.map.row_count):
            self.map_block_info[row] = {}
            for col in range(self.map.col_count):
                self.map_block_info[row][col] = {
                    "surface": None,
                    "id": i,
                    "x": 320 * col,
                    "y": 240 * row,
                    "masks": [],
                    "mask_count": 0,
                    "requested": False,
                    "received": False
                }
                i += 1
        self.masks = {}
        for i in range(self.map.mask_count):
            mask_info = self.map.get_mask_info_py(i)
            mask = Mask(i, mask_info["start_x"], mask_info["start_y"], mask_info["width"], mask_info["height"])
            mask.parent = self
            self.masks[i] = mask

        self.window = Rect((left, top), WindowSize)
        self.window_rows = math.ceil(WindowSize[1] / 240)
        self.window_cols = math.ceil(WindowSize[0] / 320)
        self.window_start_col = 0
        self.window_end_col = 0
        self.window_start_row = 0
        self.window_end_row = 0
        self.window_start_col_ext = 0
        self.window_end_col_ext = 0
        self.window_start_row_ext = 0
        self.window_end_row_ext = 0
        self.mask_in_window = []

        self.window_row_num = math.ceil(self.map.height / WindowSize[1])
        self.window_col_num = math.ceil(self.map.width / WindowSize[0])
        self.heads = {}
        for i in range(self.window_row_num):
            self.heads[i] = {}
            for j in range(self.window_col_num):
                self.heads[i][j] = {}
        self.children_in_window = []

        self.left_top = ()

        self.update_count = 0

    def handle_events(self, event):
        self.children_handle_events(event)
        if not event.handled:
            self.handle_event(event)

    def on_mouse_left_down(self, event):
        x = self.window.left + event.pos[0]
        y = self.window.top + event.pos[1]
        print(x, y)
        self.new_target(event, False)

    def on_mouse_right_down(self, event):
        self.new_target(event, True)

    def new_target(self, event, running):
        target = (self.window.left + event.pos[0], self.window.top + event.pos[1])
        path_list = self.map.find_path((role_manager.main_role.x, role_manager.main_role.y), target)
        role_manager.main_role.set_new_target(path_list, running)
        event.handled = True

        self.add_child(Throwaway("gires.wdf", "scene/walkpoint.tca", target[0], target[1]))

    def update(self, context):
        main_role = role_manager.main_role
        self.window_update(main_role.x, main_role.y)
        context.set_left_top(self.window.left, self.window.top)  # 获取地图窗口左上角
        self.left_top = self.window.left, self.window.top
        self.map_update(context)
        self.children_update(context)

    def map_update(self, context):
        self.mask_in_window = []
        no_repeat = {}
        for i in range(self.window_start_row, self.window_end_row + 1):
            for j in range(self.window_start_col, self.window_end_col + 1):
                block = self.map_block_info[i][j]
                if not block["requested"]:  # 未请求JPEG
                    self.map.read_jpeg(block["id"])  # 请求地图区块jpeg
                    block["masks"] = self.map.get_block_masks_py(block["id"])
                    block["mask_count"] = len(block["masks"])
                    block["requested"] = True
                elif not block["received"]:  # 已请求JPEG但未收到
                    if self.map.has_jpeg_loaded(block["id"]):  # 收到
                        block["received"] = True
                        block["surface"] = pg.image.frombuffer(self.map.get_jpeg_rgb(block["id"]), (320, 240), "RGB")
                        self.map.erase_jpeg_rgb(block["id"])

                for mask_index in block["masks"]:  # 请求地图区块中的mask
                    if not self.masks[mask_index].requested:  # 未请求Mask
                        self.map.read_mask(mask_index)
                        self.masks[mask_index].requested = True
                    elif not self.masks[mask_index].received:  # 已请求Mask但未收到
                        if self.map.has_mask_loaded(mask_index):
                            self.masks[mask_index].received = True
                            self.masks[mask_index].load_surface()
                            self.map.erase_mask_rgb(mask_index)
                    elif mask_index not in no_repeat:
                        no_repeat[mask_index] = True
                        self.masks[mask_index].update(context)
                        self.mask_in_window.append(self.masks[mask_index])
        self.mask_in_window.sort(key=lambda item: item.z)

    def window_update(self, x, y, directly=False):
        window_left = x - WindowSize[0] // 2
        if window_left < 0:
            window_left = 0
        elif x + WindowSize[0] // 2 > self.map.width:
            window_left = self.map.width - WindowSize[0]
        self.window_start_col = window_left // 320
        self.window_start_col_ext = max(self.window_start_col - 1, 0)
        self.window_end_col = min(self.window_start_col + self.window_cols + 1, self.map.col_count - 1)
        self.window_end_col_ext = min(self.window_end_col + 1, self.map.col_count - 1)
        window_top = y - WindowSize[1] // 2
        if window_top < 0:
            window_top = 0
        elif y + WindowSize[1] // 2 > self.map.height:
            window_top = self.map.height - WindowSize[1]
        self.window_start_row = window_top // 240
        self.window_start_row_ext = max(self.window_start_row - 1, 0)
        self.window_end_row = min(self.window_start_row + self.window_rows + 1, self.map.row_count - 1)
        self.window_end_row_ext = min(self.window_end_row + 1, self.map.row_count - 1)

        target_vector = Vector2()
        target_vector.x = window_left + WindowSize[0] // 2
        target_vector.y = window_top + WindowSize[1] // 2
        current_vector = Vector2()
        current_vector.x = self.window.centerx
        current_vector.y = self.window.centery
        if directly:
            self.window.move_ip(int(target_vector.x) - self.window.centerx, int(target_vector.y) - self.window.centery)
        else:
            new_vector = current_vector.slerp(target_vector, 0.08)
            self.window.move_ip(new_vector.x - current_vector.x, new_vector.y - current_vector.y)

    def children_update(self, context):
        self.children_in_window = []
        
        row, col = self.get_window_index(self.window.x, self.window.y)
        for i in range(row, row + 2):
            for j in range(col, col + 2):
                if i in self.heads and j in self.heads[i]:
                    objs_list = list(self.heads[i][j].values())
                    for obj in objs_list:
                        obj.update(context)
                        if isinstance(obj, Character):
                            self.character_update_z_under_mask(obj)
                        tmp_row, tmp_col = self.get_window_index(obj.x, obj.y)
                        if tmp_row != i or tmp_col != j or obj.useless:
                            self.heads[i][j].pop(obj.id)
                            if not obj.useless:
                                self.add_child(obj)
                        if not obj.useless:
                            self.children_in_window.append(obj)
        self.children_in_window.sort(key=lambda item: item.z)

    def children_handle_events(self, event):
        row, col = self.get_window_index(self.window.x, self.window.y)
        for i in range(row, row + 2):
            for j in range(col, col + 2):
                if i in self.heads and j in self.heads[i] and self.heads[i][j]:
                    objs_list = list(self.heads[i][j].values())
                    for obj in objs_list:
                        obj.handle_event(event)
                        if event.handled:
                            return

    def character_update_z_under_mask(self, character):
        char_rect = character.get_ani_rect()
        char_x = character.x
        char_y = character.y
        row, col = self.get_block_index(char_x, char_y)

        for mask_index in self.map_block_info[row][col]["masks"]:
            if self.masks[mask_index].received:
                mask = self.masks[mask_index]
                if mask.calc_sort_z(char_rect, char_x, char_y): 
                    character.z = max(character.z, mask.z + 1)

    def add_child(self, child):
        row, col = self.get_window_index(child.x, child.y)
        self.heads[row][col][child.id] = child

    def get_window_index(self, x, y):
        row = min(max(math.floor(y / WindowSize[1]), 0), self.window_row_num - 1)
        col = min(max(math.floor(x / WindowSize[0]), 0), self.window_col_num - 1)
        return row, col

    def get_block_index(self, x, y):
        row = min(math.floor(y / 240), self.map.row_count - 1)
        col = min(math.floor(x / 320), self.map.col_count - 1)
        return row, col

    def draw(self, screen):
        for i in range(self.window_start_row_ext, self.window_end_row + 1):
            for j in range(self.window_start_col_ext, self.window_end_col + 1):
                block = self.map_block_info[i][j]
                if block["received"]:
                    screen.blit(block["surface"], (block["x"] - self.left_top[0], block["y"] - self.left_top[1]))

        area = pg.surface.Surface(WindowSize, flags=pg.SRCALPHA)
        render_items = self.mask_in_window + self.children_in_window
        render_items.sort(key=lambda t: t.z)
        for item in render_items:
            item.draw(area)
        screen.blit(area, (0, 0))

    def blit_cell(self):
        for i in range(self.map.cell_row_count):
            for j in range(self.map.cell_col_count):
                if self.map.cell[i, j] > 1:
                    pg.draw.rect(self.cell_surface, (255, 0, 0, 150), Rect((j * 20, i * 20), (20, 20)))

    def draw_cell(self, screen):
        screen.blit(self.cell_surface, (0, 0), self.window)

    def destroy(self):
        super().destroy()
        self.map.drop_map()
