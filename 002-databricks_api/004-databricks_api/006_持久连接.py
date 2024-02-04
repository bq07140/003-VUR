from databricks import sql
from dbutils.persistent_db import PersistentDB

# 定义数据库连接参数
db_config = {
    "server_hostname": "adb-2515004071041721.1.databricks.azure.cn",
    "http_path": "/sql/1.0/warehouses/07194f39c23cde02",
    "access_token": "dapi9aefab090c8d18b7619235656a43b0ef"
}

# 创建数据库连接池
db_pool = PersistentDB(
    sql.connect,
    maxusage=None,  # 不限制连接的重复使用次数
    **db_config
)

# 获取连接
conn = db_pool.connection()
cursor = conn.cursor()

# 执行查询
cursor.execute("SELECT * FROM hive_metastore.default.dw_gdc_daily LIMIT 5;")
ret = cursor.fetchall()

# 处理查询结果
for line in ret:
    print(line)

# 关闭游标和连接
cursor.close()
conn.close()

# 注意：这里不需要关闭数据库连接池，因为它是持久的，会一直存在。


