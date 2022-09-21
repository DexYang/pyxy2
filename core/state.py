import weakref
from core.ref import Ref


class State(Ref):
    def __init__(self):
        super().__init__()
        self._parent = None

    @property
    def parent(self):
        return None if self._parent is None else self._parent()

    @parent.setter
    def parent(self, node):
        self._parent = weakref.ref(node)

    def update(self, context):
        pass
