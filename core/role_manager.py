from core.ref import Ref
from db.role import get_roles, create_roles
from core.animated.character import Character


class RoleManager(Ref):
    _instance = None

    def __new__(cls):
        if not hasattr(cls, '_instance') or cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.username = None
        self.roles = {}
        self._main_role = None

    def login(self, username):
        self.username = username
        self.roles = {}

    def get_roles(self):
        if not self.username:
            return self.emit("tip", text="#Y用户未登录")
        db_roles = get_roles(self.username)
        self.roles = {}
        for r in db_roles: 
            self.roles[r.doc_id] = r

    def create_role(self, role):
        create_roles(self.username, role)

    def select(self, role_id):
        self.main_role  = Character(self.roles[role_id]["shape"], self.roles[role_id]["x"], self.roles[role_id]["y"])
        self.emit("change_scene", scene_name="World", map_id=self.roles[role_id]["map_id"])

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
