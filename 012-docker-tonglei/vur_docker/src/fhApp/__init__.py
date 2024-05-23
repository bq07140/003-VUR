# -*- coding: utf-8 -*-
import os
# import logging
# from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_cors import *
from config import config_dict, static_folder

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def setup_log(leave_name):
    """根据不同的环境，指定不同的日志等级"""

    # # 设置日志的记录等级
    # logging.basicConfig(level=leave_name)  # 调试debug级
    # # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    # file_log_handler = RotatingFileHandler(os.path.join(BASE_DIR, "logs/log"), maxBytes=1024 * 1024 * 100, backupCount=10)
    # # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    # formatter = logging.Formatter('%(asctime)s-%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # # 为刚创建的日志记录器设置日志记录格式
    # file_log_handler.setFormatter(formatter)
    # # 为全局的日志工具对象（flask app使用的）添加日志记录器
    # logging.getLogger().addHandler(file_log_handler)

    pass


# 创建工厂方法
def create_app(config_name):
    config_cls = config_dict[config_name]
    # 添加日志
    # setup_log(config_cls.LOG_LEVEL)

    app = Flask(__name__, static_folder="../" + static_folder)
    # 跨域
    CORS(app, supports_credentials=True)

    app.config.from_object(config_cls)

    # 导入蓝图ss
    from .api import api
    app.register_blueprint(api)
    return app




