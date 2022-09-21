import logging


def logger_factory(file_log_level, console_log_level):
    # 配置日志
    formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] [%(module)s] [%(funcName)s] [%(lineno)d] - %(message)s')
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)
    # # 文件日志
    # handler = logging.FileHandler("logging_%s.log" % time.strftime("%Y-%m-%d", time.localtime()))
    # handler.setLevel(file_log_level)
    # handler.setFormatter(formatter)
    # _logger.addHandler(handler)
    # 命令行日志
    console = logging.StreamHandler()
    console.setLevel(console_log_level)
    console.setFormatter(formatter)

    _logger.addHandler(console)
    return _logger


logger = logger_factory(file_log_level=logging.INFO, console_log_level=logging.DEBUG)
