#!/usr/bin/env python
# coding:utf-8
"""
@author : tanwengang
@file : redis_connect_server.py
@time : 2023/9/27 16:26
@desc :
"""

from .db_config import sql_warehouse_config
from databricks import sql
from dbutils.persistent_db import PersistentDB


# 创建数据库连接池
DB_POOL = PersistentDB(
    sql.connect,
    maxusage=None,  # 不限制连接的重复使用次数
    **sql_warehouse_config
)







