from core.ref import Ref


class RoleManager(Ref):
    _instance = None

    def __new__(cls):
        if not hasattr(cls, '_instance') or cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self._main_role = None

    @property
    def main_role(self):
        return self._main_role

    @main_role.setter
    def main_role(self, main_role):
        self._main_role = main_role

    def set_main_role_new_target(self, path_list, running):
        self.main_role.set_new_target(path_list, running)

    def load_into(self, scene):
        if hasattr(scene, "world_layer"):
            scene.world_layer.add_child(self.main_role)


role_manager = RoleManager()
