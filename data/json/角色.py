from data.character import characters, 种族, 性别


def get(char_id, role_name):
    return {
        "shape": char_id,
        "photo": char_id,

        "名字": role_name,
        "称谓": [
            "pyxy2一员"
        ],
        "已选称谓": 0,

        "角色名": characters[char_id]['角色名'],
        "性别": characters[char_id]['性别'],
        "种族": characters[char_id]['种族'],
        "门派": characters[char_id]['门派'],
        "武器": characters[char_id]['武器'],
        "等级": 0,
        "转生": 0,
        "银子": 100000,
        "存银": 0,
        "战绩": 0,
        "声望": 0,

        "潜力": 0,

        "气血": 80,
        "最大气血": 100,
        "根骨": 0,

        "法力": 50,
        "最大法力": 100,
        "灵性": 0,

        "攻击": 200,
        "力量": 0,

        "速度": 200,
        "敏捷": 0,

        "经验": 1800,

        "map_id": 1001,
        "x": 5100,
        "y": 4200,

        "已选召唤兽": -1,
        "召唤兽": [
        ]
    }