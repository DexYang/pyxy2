from ctypes import *
import numpy
import threading
pyxy2 = cdll.LoadLibrary("lib/pyxy2.dll")


pyxy2.read_pal.argtype = [c_void_p]
pyxy2.read_pal.restype = POINTER(c_char * 1024)

pyxy2.get_hash_py.argtype = [c_void_p]
pyxy2.get_hash_py.restype = py_object


def read_pal(data):
    res = pyxy2.read_pal(data)
    _bytes = res.contents.raw
    return _bytes


def read_frame(data, color_board, size):
    pyxy2.read_frame.argtype = [c_void_p, c_void_p]
    pyxy2.read_frame.restype = POINTER(c_char * size)
    
    res = pyxy2.read_frame(data, color_board)
    _bytes = res.contents.raw
    return _bytes


def get_hash_py(path):
    pyxy2.get_hash_py.argtype = [c_void_p]
    pyxy2.get_hash_py.restype = py_object
    res = pyxy2.get_hash_py(path.encode("GBK"))
    return res


class MapThread(threading.Thread):
    def run(self):
        pyxy2.loop()


def end_loop():
    pyxy2.end_loop()


def add_task(map_path, index, _type):
    # type  0 -> JPEG   1/2 -> Mask   
    pyxy2.add_task.argtype = [c_void_p, c_int, c_int]
    pyxy2.add_task(map_path.encode('GBK'), index, _type)


def get_map_info_py(map_path):
    pyxy2.get_map_info_py.argtype = c_void_p
    pyxy2.get_map_info_py.restype = py_object
    return pyxy2.get_map_info_py(map_path.encode('GBK'))


def drop_map(map_path):
    pyxy2.drop_map.argtype = c_void_p
    pyxy2.drop_map(map_path.encode('GBK'))


def get_map_cell(map_path, row, col):
    pyxy2.get_map_cell.argtype = c_void_p
    pyxy2.get_map_cell.restype = POINTER(c_int * (row * col))
    res = pyxy2.get_map_cell(map_path.encode('GBK'))
    return numpy.array(res.contents, dtype=numpy.float32).reshape((row, col)) * 9999.0 + 1.0


# JPEG
def get_block_masks_py(map_path, index):
    pyxy2.get_block_masks_py.argtype = [c_void_p, c_int]
    pyxy2.get_block_masks_py.restype = py_object
    res = pyxy2.get_block_masks_py(map_path.encode('GBK'), index)
    return res


def has_jpeg_loaded(map_path, index):
    pyxy2.has_jpeg_loaded.argtype = [c_void_p, c_int]
    pyxy2.has_jpeg_loaded.restype = c_bool
    res = pyxy2.has_jpeg_loaded(map_path.encode('GBK'), index)
    return res


def get_jpeg_rgb(map_path, index):
    pyxy2.get_jpeg_rgb.argtype = [c_void_p, c_int]
    pyxy2.get_jpeg_rgb.restype = POINTER(c_char * 230400)
    res = pyxy2.get_jpeg_rgb(map_path.encode('GBK'), index)
    _bytes = res.contents.raw
    return _bytes


def erase_jpeg_rgb(map_path, index):
    pyxy2.erase_jpeg_rgb.argtype = [c_void_p, c_int]
    pyxy2.erase_jpeg_rgb(map_path.encode('GBK'), index)


# Mask
def get_mask_info_py(map_path, index):
    pyxy2.get_mask_info_py.argtype = [c_void_p, c_int]
    pyxy2.get_mask_info_py.restype = py_object
    res = pyxy2.get_mask_info_py(map_path.encode('GBK'), index)
    return res


def has_mask_loaded(map_path, index):
    pyxy2.has_mask_loaded.argtype = [c_void_p, c_int]
    pyxy2.has_mask_loaded.restype = c_bool
    res = pyxy2.has_mask_loaded(map_path.encode('GBK'), index)
    return res


def get_mask_rgba(map_path, index, size):
    pyxy2.get_mask_rgba.argtype = [c_void_p, c_int]
    pyxy2.get_mask_rgba.restype = POINTER(c_char * size)
    res = pyxy2.get_mask_rgba(map_path.encode('GBK'), index)
    _bytes = res.contents.raw
    return _bytes


def erase_mask_rgb(map_path, index):
    pyxy2.erase_mask_rgb.argtype = [c_void_p, c_int]
    pyxy2.erase_mask_rgb(map_path.encode('GBK'), index)
