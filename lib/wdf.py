from lib.was import WAS
from lib.pyxy2 import get_hash_py
from utils.logger import logger


class WDF:
    def __init__(self, wdf: str) -> None:
        self.wdf = wdf

        self.n = 0
        self.hash_table = {}

        self.file = open(self.wdf, 'rb')
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

    def get(self, path_or_hash: str, pal: bytes = None):
        if isinstance(path_or_hash, int): 
            _hash = path_or_hash
        else: 
            _hash: int
            if path_or_hash.startswith("0x"):
                _hash = int(path_or_hash, base=16)
            else:
                _hash = get_hash_py(path_or_hash)
        logger.info("资源路径{}, {}, HASH值{}".format(self.wdf, path_or_hash, hex(_hash)))
        
        if _hash not in self.hash_table: 
            logger.info("资源路径{}, {}, HASH值{} 不存在".format(self.wdf, path_or_hash, _hash))
        item = self.hash_table[_hash]
        with open(self.wdf, 'rb') as file:
            file.seek(item["offset"])
            flag = file.read(2)
        
            if flag == b'SP':
                return WAS(self.wdf, item["offset"], item["size"], pal)
            else:
                file.seek(item["offset"])
                data = file.read(item["size"])
                return WDFItem(flag, data, item["size"])

    def get_32(self) -> int:
        return int.from_bytes(self.file.read(4), "little")

    def get_16(self) -> int:
        return int.from_bytes(self.file.read(2), "little")


class WDFItem: 
    def __init__(self, _type, _data, _size):
        self.type  = _type
        self.data = _data
        self.size = _size