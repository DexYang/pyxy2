from lib.was import WAS
from lib.pyxy2 import get_hash_py
from settings import XY2PATH

class WDF:
    def __init__(self, wdf: str) -> None:
        self.wdf = wdf
        self.path = XY2PATH + wdf

        self.n = 0
        self.hash_table = {}

        self.file = open(self.path, 'rb')
        if self.file.read(4) != b'PFDW':  # WDF文件标志
            raise TypeError("Not WDF File")
        self.n = self.get_32()

        offset = self.get_32()
        self.file.seek(offset)
        for _ in range(self.n):
            _hash = self.get_32()
            _offset = self.get_32()
            _size = self.get_32()
            _spaces = self.get_32()
            self.hash_table[_hash] = {
                "hash": _hash, 
                "offset": _offset, 
                "size": _size, 
                "spaces": _spaces}

        self.file.close()

    def get(self, s: str, pal: bytes = None):
        _hash: int
        if s.startswith("0x"):
            _hash = int(s, base=16)
        else:
            _hash = get_hash_py(s)

        self.file = open(self.path, 'rb')
        
        item = self.hash_table[_hash]
        self.file.seek(item["offset"])
        flag = self.file.read(2)
        self.file.close()

        if flag == b'SP':
            return WAS(self.wdf, item["offset"], item["size"], pal)
        

    def get_32(self) -> int:
        return int.from_bytes(self.file.read(4), "little")

    def get_16(self) -> int:
        return int.from_bytes(self.file.read(2), "little")