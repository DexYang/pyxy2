from data.character import characters, 种族, 性别
from data.json.召唤兽 import get召唤兽


def get角色(char_id, role_name):
    res = {
        "shape": char_id,
        "photo": char_id,

        "名字": role_name,
        "称谓": [
            "大话西游一员"
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

        "map_name": "老长安",
        "x": 5100,
        "y": 4200,

        "已选召唤兽": -1,
        "召唤兽": [
        ]
    }

    res["召唤兽"].append(get召唤兽(2060))
    return res