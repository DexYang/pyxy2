from lib.pyxy2 import read_frame, read_pal
from settings import XY2PATH


class WAS:
    def __init__(self, path: str, offset: int = 0, size: int = 0, pal: bytes = None) -> None:
        self.path = XY2PATH + path
        self.offset = offset
        self.size = size

        self.file = open(self.path, 'rb')
        if self.size == 0:
            self.file.seek(0, 2)
            self.size = self.file.tell()
        self.file.seek(self.offset)

        if self.file.read(2) != b'SP':  # WDF文件标志
            raise TypeError("Not WAS File")

        self.head_size = self.get_16()
        self.direction_num = self.get_16()
        self.frame_num = self.get_16()
        self.pic_num = self.direction_num * self.frame_num
        self.width = self.get_16()
        self.height = self.get_16()
        self.x = self.get_16()
        self.y = self.get_16()

        self.time = []
        if self.head_size > 12:
            for _ in range(self.head_size - 12):
                self.time.append(self.get_8())

        self.pal = self.file.read(512)
        if pal:
            self.pal = pal
        self.pal = read_pal(self.pal)

        self.pic_offsets = []
        for _ in range(self.pic_num):
            self.pic_offsets.append(self.get_32() + self.offset + 4 + self.head_size)

        self.frames = []
        for i in range(self.direction_num):
            self.frames.append([])
            for j in range(self.frame_num): 
                index = i * self.frame_num + j
                self.file.seek(self.pic_offsets[index])

                _x = self.get_32()
                _y = self.get_32()
                _w = self.get_32()
                _h = self.get_32()

                frame_size: int
                if index < self.pic_num - 1:
                    frame_size = self.pic_offsets[index + 1] - self.pic_offsets[index]
                else:
                    frame_size = self.size + self.offset - self.pic_offsets[index]

                self.file.seek(self.pic_offsets[index])
                buff = self.file.read(frame_size)
                
                data = read_frame(buff, self.pal, _w * _h * 4)

                frame = {"x": _x, "y": _y, "width": _w, "height": _h, "data": data}
                self.frames[i].append(frame)
    
        self.file.close()

        
    def get_32(self) -> int:
        return int.from_bytes(self.file.read(4), "little")

    def get_16(self) -> int:
        return int.from_bytes(self.file.read(2), "little")

    def get_8(self) -> int:
        return int.from_bytes(self.file.read(1), "little")