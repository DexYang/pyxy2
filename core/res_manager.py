from distutils import filelist
import os
import time
import pygame as pg
from io import BytesIO

from lib.wdf import WDF, WDFItem, get_hash_py
from lib.was import WAS
from settings import XY2PATH
from utils.logger import logger


class ResManager:
    _instance = None

    def __new__(cls):
        if not hasattr(cls, '_instance') or cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.pool = {}
        self.wdfs = {}
        self.wdf_hash = {}
        self.travel(XY2PATH)

    def travel(self, filepath):
        file_list = list(filter(lambda item: item.is_file() and item.name.find(".wd") != -1, list(os.scandir(filepath))))
        file_list.sort(key=lambda item: item.name[-1] if item.name[-1] != 'f' else '0')
        
        for file in file_list:
            origin_name = file.name 
            wdf_name = file.name[:-4]
            try:
                if origin_name not in self.wdfs:
                    self.wdfs[origin_name] = WDF(XY2PATH + origin_name)
                if wdf_name not in self.wdf_hash:
                    self.wdf_hash[wdf_name] = {}
                for _hash in self.wdfs[origin_name].hash_table.keys():
                    if _hash not in self.wdf_hash[wdf_name]:
                        self.wdf_hash[wdf_name][_hash] = []
                    self.wdf_hash[wdf_name][_hash].append(origin_name)
            except TypeError:
                continue

    def get(self, wdf: str, path_or_hash, name="", pal=None, oldFirst=True):
        now = time.time()
        if name == "":
            name = wdf + ":" + path_or_hash
        if name in self.pool:
            self.pool[name][1] = now
            return self.pool[name][0]

        if wdf.find(".wd") != -1:  # 直接选定wdf文件
            if wdf not in self.wdfs:
                self.wdfs[wdf] = WDF(XY2PATH + wdf)
            item = self.wdfs[wdf].get(path_or_hash, pal)
        else:  
            path = XY2PATH + wdf + "/" + path_or_hash
            if os.path.exists(path):  # 优先直接读取零散的资源文件
                with open(self.wdf, 'rb') as file:
                    flag = file.read(2)
                    if flag == b'SP':
                        item = WAS(path)
                    else: 
                        file.seek(0, 2)
                        size = self.file.tell()
                        file.seek(0)
                        data = file.read(size)
                        item = WDFItem(flag, data, size)
            else:  # 读取WDF
                if path_or_hash.startswith("0x"):
                    _hash = int(path_or_hash, base=16)
                else:
                    _hash = get_hash_py(path_or_hash)
                if wdf not in self.wdf_hash: 
                    logger.info("WDF 文件不存在: " + wdf)
                    return
                if _hash not in self.wdf_hash[wdf]: 
                    logger.info("Hash或者Path不存在: " + path_or_hash)
                    return 
                origin_wdf = self.wdf_hash[wdf][_hash][0 if oldFirst else -1]
                item = self.wdfs[origin_wdf].get(path_or_hash, pal)
        
        if isinstance(item, WAS):
            self.pool[name] = [item, now]

        elif item.type == b'\x00\x00':
            self.pool[name] = [pg.image.load(BytesIO(item.data), "tga"), now]

        elif item.type == b'\x4d\x42':
            self.pool[name] = [pg.image.load(BytesIO(item.data), "bmp"), now]

        elif item.type == b'\xff\xd8':
            self.pool[name] = [pg.image.load(BytesIO(item.data), "jpg"), now]

        elif item.type == b'\x20\x50':
            chats = []
            for c in item.data.split(b"\x50\x20\x4e\x0d\x0a")[1:]:
                chats.append(c.decode("gbk"))
            self.pool[name] = [chats, now]
        else:
            self.pool[name] = [item, now]

        return self.pool[name][0]



res_manager = ResManager()