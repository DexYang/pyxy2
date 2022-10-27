import pygame as pg
from pygame import Rect

from core.animation import Animation
from core.res_manager import res_manager, WAS


def get_surface(wdf: str, was_hash: str | int) -> pg.Surface: 
    item = res_manager.get(wdf, was_hash)
    if isinstance(item, WAS):
        item = Animation(item)
        surface = item.get_current_frame().surface
    else:
        surface = item
    return surface


def scale9_was(wdf: str, was_hash: str | int, w: int, h: int = 0, _len: int = 20):
    surface = get_surface(wdf, was_hash)
    return scale9_surf(surf=surface, w=w, h=h, _len=_len)


def scale9_surf(surf: pg.Surface, w: int, h: int = 0, _len: int = 20):

    _rect = surf.get_rect()
    ow = _rect.width
    oh = _rect.height

    mid_w = ow - _len * 2
    mid_h = oh - _len * 2

    if mid_h <= 0:
        return scale_horizontal(surf, w)

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
        temp_top = pg.Surface((w_need_to_blit, _len), pg.SRCALPHA)
        temp_bottom = pg.Surface((w_need_to_blit, _len), pg.SRCALPHA)
        _x = 0
        while _x < w_need_to_blit:
            temp_top.blit(mid_top, (_x, 0))
            temp_bottom.blit(mid_bottom, (_x, 0))
            _x += mid_w
        mid_top = temp_top
        mid_bottom = temp_bottom
    else:
        mid_top = mid_top.subsurface(Rect((0, 0), (w - 2 * _len, _len)))
        mid_bottom = mid_bottom.subsurface(Rect((0, 0), (w - 2 * _len, _len)))

    if h > oh:
        h_need_to_blit = h - 2 * _len
        temp_left = pg.Surface((_len, h_need_to_blit), pg.SRCALPHA)
        temp_right = pg.Surface((_len, h_need_to_blit), pg.SRCALPHA)
        _y = 0
        while _y < h_need_to_blit:
            temp_left.blit(left, (0, _y))
            temp_right.blit(right, (0, _y))
            _y += mid_h
        left = temp_left
        right = temp_right
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


def scale_horizontal(surf: pg.Surface, w: int):
    _rect = surf.get_rect()
    ow = _rect.width
    oh = _rect.height

    mid_w = ow - oh * 2

    left = surf.subsurface(Rect((0, 0), (oh, oh)))
    mid = surf.subsurface(Rect((oh, 0), (mid_w, oh)))
    right = surf.subsurface(Rect((ow - oh, 0), (oh, oh)))

    _surf = pg.Surface((w, oh), pg.SRCALPHA)
    _surf.blit(left, (0, 0))
    _surf.blit(right, (w - oh, 0))

    if w > ow:
        w_need_to_blit = w - 2 * oh
        temp_mid = pg.Surface((w_need_to_blit, oh), pg.SRCALPHA)
        
        _x = 0
        while _x < w_need_to_blit:
            temp_mid.blit(mid, (_x, 0))
            _x += mid_w
        mid = temp_mid
    else:
        mid = mid.subsurface(Rect((0, 0), (w - 2 * oh, oh)))

    _surf.blit(mid, (oh, 0))

    return _surf


def scale9_combination(w: int, h: int, **kwargs):
    _surf = pg.Surface((w, h), pg.SRCALPHA)

    上: pg.Surface = get_surface(**kwargs.get("上"))
    下: pg.Surface = get_surface(**kwargs.get("下"))
    左: pg.Surface = get_surface(**kwargs.get("左"))
    右: pg.Surface = get_surface(**kwargs.get("右"))
    左上: pg.Surface = get_surface(**kwargs.get("左上"))
    左下: pg.Surface = get_surface(**kwargs.get("左下"))
    右上: pg.Surface = get_surface(**kwargs.get("右上"))
    右下: pg.Surface = get_surface(**kwargs.get("右下"))
    底: pg.Surface = get_surface(**kwargs.get("底"))
    花: pg.Surface = get_surface(**kwargs.get("花", kwargs.get("底")))

    _rect = 底.get_rect()
    ow = _rect.width
    oh = _rect.height

    _x = 0
    _y = 0
    while _y < h:
        while _x < w:
            _surf.blit(底, (_x, _y))
            _surf.blit(花, (_x, _y))
            _x += ow
        _x = 0
        _y += oh

    _x = 0
    while _x < w:
        _surf.blit(上, (_x, 0))
        _surf.blit(下, (_x, h - 下.get_rect().height))
        _x += ow

    _y = 0
    while _y < h:
        _surf.blit(左, (0, _y))
        _surf.blit(右, (w - 右.get_rect().width, _y))
        _y += oh

    _surf.blit(左上, (0, 0))
    _surf.blit(左下, (0, h - 左下.get_rect().height))
    _surf.blit(右上, (w - 右上.get_rect().width, 0))
    _surf.blit(右下, (w - 右下.get_rect().width, h - 右下.get_rect().height))

    return _surf
