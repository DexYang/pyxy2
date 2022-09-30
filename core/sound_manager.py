from lib import pyfmodex
from lib.pyfmodex.flags import MODE
from lib.pyfmodex.structures import CREATESOUNDEXINFO
from core.res_manager import res_manager
import settings

system = pyfmodex.System()
system.init()


class SoundManager:
    _instance = None

    def __new__(cls):
        if not hasattr(cls, '_instance') or cls._instance is None:
            
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.bg_music = None
        self.music_wdf = ""
        self.music_hash = ""

        self.loop_sound = []

    def play(self, wdf, _hash, loop=False):
        sound = self.get_sound(wdf, _hash, loop)
        channel = sound.play()
        channel.volume = settings.SOUND / 100
        if loop:
            self.loop_sound.append(channel)

    def music(self, wdf, _hash):
        if self.music_wdf == wdf and self.music_hash == _hash:
            return
        if settings.BGM <= 0:
            return
        if self.bg_music and self.bg_music.is_playing:
            self.bg_music.stop()
        sound = self.get_sound(wdf, _hash, True)
        self.bg_music = sound.play()
        self.bg_music.volume = settings.BGM / 100
        self.music_wdf = wdf
        self.music_hash = _hash

    def get_sound(self, wdf, _hash, loop=False):
        loop_mode = MODE.LOOP_NORMAL if loop else MODE.LOOP_OFF
        item = res_manager.get(wdf, _hash)
        sound = system.create_sound(item.data,
                            mode=MODE.OPENMEMORY | loop_mode,
                            exinfo=CREATESOUNDEXINFO(length=item.size))
        return sound

    def stop_loop_sound(self):
        for sound in self.loop_sound:
            if sound.is_playing:
                sound.stop()
        self.loop_sound = []

    def pause_loop_sound(self):
        for sound in self.loop_sound:
            sound.pause()
        settings.SOUND = -1

    def play_loop_sound(self):
        if settings.SOUND > 0:
            for sound in self.loop_sound:
                sound.play()       

    def set_loop_sound_volume(self, volume):
        for sound in self.loop_sound:
            sound.volume = volume / 100
        settings.SOUND = volume

    def stop_bgm(self):
        if self.bg_music:
            self.bg_music.stop()
        settings.BGM = -1

    def pause_bgm(self):
        if self.bg_music:
            self.bg_music.pause()
        settings.BGM = -1

    def play_bgm(self):
        if self.bg_music and settings.BGM > 0:
            self.bg_music.play()
            self.bg_music.volume = settings.BGM

    def set_bgm_volume(self, volume):
        if self.bg_music:
            self.bg_music.volume = volume / 100
        settings.BGM = volume


SOUND_MANAGER = SoundManager()