from core.ui.node import Blank



class WindowLayer(Blank):
    def __init__(self, name=None, x=0, y=0, w=0, h=0, z=0):
        super().__init__(name, x, y, w, h, z)
        self.max_z = -999999999999999

    def on_open_dialog(self, event):
        
        print(event.title)
        for k, v in event.options.items():
            print(k)
            v()
        event.handled = True