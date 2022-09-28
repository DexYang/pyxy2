import configparser

# 实例化一个 ConfigParser 实例
config = configparser.ConfigParser()
# 打开 ini 文件
config.read("settings.ini", encoding="utf-8")

XY2PATH = config["配置"].get("path")
UI= config["配置"].get("ui")

WindowSize = (800, 600)



AnimationRate = 80
RunningSpeed = 4
WalkingSpeed = 2
