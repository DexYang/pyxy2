import pygame as pg
from io import BytesIO
from lib.wdf import WDF
from lib.was import WAS
from settings import XY2PATH


class ResManager:
    _instance = None

    def __new__(cls):
        if not hasattr(cls, '_instance') or cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.pool = {}
        self.wdfs = {}

    def get(self, wdf: str, path_or_hash, name="", pal=None):
        if name == "":
            name = wdf + ":" + path_or_hash

        if name in self.pool:
            return self.pool[name]

        if wdf.find(".wd") != -1:

            if wdf not in self.wdfs:
                self.wdfs[wdf] = WDF(XY2PATH + wdf)

            item = self.wdfs[wdf].get(path_or_hash, pal)

        else:
            if path_or_hash.endswith(".tcp") or path_or_hash.endswith(".tca"):
                item = WAS("res/"+wdf+"/"+path_or_hash)

        
        if isinstance(item, WAS):
            self.pool[name] = item
            return item
        elif item.type == b'\x00':
            return pg.image.load(BytesIO(item.data), "tga")
        elif item.type == b'\x4d\x42':
            return pg.image.load(BytesIO(item.data), "bmp")
        elif item.type == b'\xff\xd8':
            return pg.image.load(BytesIO(item.data), "jpg")
        elif item.type == b'\x20\x50':
            chats = []
            for c in item.data.split(b"\x50\x20\x4e\x0d\x0a")[1:]:
                chats.append(c.decode("gbk"))
            return chats
        else:
            return item


res_manager = ResManager()