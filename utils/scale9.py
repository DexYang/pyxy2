from re import S
import pygame as pg
from pygame import Rect

from core.animation import Animation
from core.res_manager import res_manager, WAS


def scale9_was(wdf: str, was_hash: str | int, w: int, h: int, _len: int = 20):
    item = res_manager.get(wdf, was_hash)
    if isinstance(item, WAS):
        item = Animation(item)
        surface = item.get_current_frame().surface
    else:
        surface = item
    return scale9_surf(surf=surface, w=w, h=h, _len=_len)


def scale9_surf(surf: pg.Surface, w: int, h: int, _len: int = 20):

    _rect = surf.get_rect()
    ow = _rect.width
    oh = _rect.height

    mid_w = ow - _len * 2
    mid_h = oh - _len * 2

    left_top = surf.subsurface(Rect((0, 0), (_len, _len)))
    mid_top = surf.subsurface(Rect((_len, 0), (mid_w, _len)))
    right_top = surf.subsurface(Rect((ow - _len, 0), (_len, _len)))

    left = surf.subsurface(Rect((0, _len), (_len, mid_h)))
    mid = surf.subsurface(Rect((_len, _len), (mid_w, mid_h)))
    right = surf.subsurface(Rect((ow - _len, _len), (_len, mid_h)))

    left_bottom = surf.subsurface(Rect((0, oh - _len), (_len, _len)))
    mid_bottom = surf.subsurface(Rect((_len, oh - _len), (mid_w, _len)))
    right_bottom = surf.subsurface(Rect((ow - _len, oh - _len), (_len, _len)))

    _surf = pg.Surface((w, h), pg.SRCALPHA)
    _surf.blit(left_top, (0, 0))
    _surf.blit(right_top, (w - _len, 0))
    _surf.blit(left_bottom, (0, h - _len))
    _surf.blit(right_bottom, (w - _len, h - _len))

    if w > ow:
        w_need_to_blit = w - 2 * _len
        temp = pg.Surface((w_need_to_blit, _len), pg.SRCALPHA)
        _x = 0
        while _x < w_need_to_blit:
            temp.blit(mid_top, (_x, 0))
            _x += mid_w
        mid_top = temp

        temp = pg.Surface((w_need_to_blit, _len), pg.SRCALPHA)
        _x = 0
        while _x < w_need_to_blit:
            temp.blit(mid_bottom, (_x, 0))
            _x += mid_w
        mid_bottom = temp
    else:
        mid_top = mid_top.subsurface(Rect((0, 0), (w - 2 * _len, _len)))
        mid_bottom = mid_bottom.subsurface(Rect((0, 0), (w - 2 * _len, _len)))

    if h > oh:
        h_need_to_blit = h - 2 * _len
        temp = pg.Surface((_len, h_need_to_blit), pg.SRCALPHA)
        _y = 0
        while _y < h_need_to_blit:
            temp.blit(left, (0, _y))
            _y += mid_h
        left = temp

        temp = pg.Surface((_len, h_need_to_blit), pg.SRCALPHA)
        _y = 0
        while _y < h_need_to_blit:
            temp.blit(right, (0, _y))
            _y += mid_h
        right = temp
    else:
        left = left.subsurface(Rect((0, 0), (_len, h - 2 * _len)))
        right = right.subsurface(Rect((0, 0), (_len, h - 2 * _len)))

    if w > ow or h > oh:
        w_need_to_blit = w - 2 * _len
        h_need_to_blit = h - 2 * _len
        temp = pg.Surface((max(w_need_to_blit, 0), max(h_need_to_blit, 0)), pg.SRCALPHA)
        _x = 0
        _y = 0
        while _y < h_need_to_blit:
            while _x < w_need_to_blit:
                temp.blit(mid, (_x, _y))
                _x += mid_w
            _x = 0
            _y += mid_h
        mid = temp
    else:
        mid = mid.subsurface(Rect((0, 0), (w - 2 * _len, h - 2 * _len)))

    _surf.blit(mid_top, (_len, 0))
    _surf.blit(mid_bottom, (_len, h - _len))
    _surf.blit(left, (0, _len))
    _surf.blit(right, (w - _len, _len))
    _surf.blit(mid, (_len, _len))

    return _surf
