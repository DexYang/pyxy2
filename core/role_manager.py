from core.ref import Ref
from db.role import get_roles, create_roles, update_role
from db.user import login, logout
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

        self.main_role = None
        self.main_role_id = 0

    def login(self, username):
        self.username = username
        self.roles = {}
        login(self.username)

    def logout(self):
        if self.username:
            self.update_roles()
            logout(self.username)
            self.username = None
            self.roles = {}

    def get_roles(self):
        if not self.username:
            return self.emit("tip", text="#Y用户未登录")
        db_roles = get_roles(self.username)
        self.roles = {}
        for r in db_roles: 
            self.roles[r.doc_id] = r

    def update_roles(self):
        if self.username:
            for _, v in self.roles.items():
                update_role(self.username, v)

    def role(self, doc_id):
        return self.roles.get(doc_id)

    def create_role(self, role):
        create_roles(self.username, role)

    def enter_world(self, role_id):
        character = Character(self.roles[role_id]["shape"], self.roles[role_id], self.roles[role_id]["x"], self.roles[role_id]["y"])
        self.set_main_role(character, role_id)
        self.emit("change_scene", scene_name="World", map_id=self.roles[role_id]["map_id"])

    def change_world(self, map_id, x, y):
        self.main_role.data["map_id"] = map_id
        self.main_role.x = x
        self.main_role.y = y
        self.main_role.reset_target()
        self.emit("change_scene", scene_name="World", map_id=map_id)

    def set_main_role(self, character, role_id):
        self.main_role = character
        self.main_role_id = role_id
        self.emit("change_status")

    def load_into(self, scene):
        if hasattr(scene, "world_layer"):
            scene.world_layer.add_child(self.main_role)

    def on_every_30s(self, event):
        self.update_roles()


role_manager = RoleManager()
