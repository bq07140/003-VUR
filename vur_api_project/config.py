# -*- coding: utf-8 -*-
import logging

# router = "/dbr/"
router = "/"
static_folder = "screen"

# 配置项目启动参数 todo 更换项目启动参数
ProjectConfig = {
    # 生产上可以把"development"改为"production",区别在于是否是debug模式
    "mode": "development",
    # 启动的ip,默认本机
    "host": "0.0.0.0",
    # 启动端口
    "port": 5000,
    # 启动进程数
    "processes": 1
}


class DevelopmentConfig(object):
    DEBUG = True
    LOG_LEVEL = logging.INFO


class ProductionConfig(object):
    DEBUG = False
    LOG_LEVEL = logging.WARNING


config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
