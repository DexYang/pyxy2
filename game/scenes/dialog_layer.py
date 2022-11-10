from core.ui.node import Blank


class DialogLayer(Blank):
    def on_open_dialog(self, event):
        print('??????')
        event.handled = True