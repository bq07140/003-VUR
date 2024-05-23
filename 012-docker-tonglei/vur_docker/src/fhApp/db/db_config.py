# 定义数据库连接参数
sql_warehouse_config = {
    "server_hostname": "adb-2515004071041721.1.databricks.azure.cn",
    "http_path": "/sql/1.0/warehouses/07194f39c23cde02",
    "access_token": "dapideac683303ce305bcf4971b955c39bbf"  #    dapi9aefab090c8d18b7619235656a43b0ef
}


# 1. 测试数据mysql链接配置


# 2. 生产数据mysql链接配置



# # 连接redis配置
# RedisCfg = {
#     "startup_nodes_jd": [
#         {"host": "39.107.107.149", "port": 6379}],  # 嘉定
#     "startup_nodes_wgq": [
#         {"host": "39.107.107.149", "port": 6379},  # 外高桥
#     ],
#     "pass_wd": r""
# }




































# # TODO 修改数据库配置
# DatabaseConfig = \
#     {
#         "dbuser": "root",
#         "dbpassword": "1234",
#         "dbhost": "127.0.0.1",
#         "dbport": 3306,
#         "dbname": "qshop_0826"
#     }
#
# # DatabaseConfig = \
# #     {
# #         "dbuser": "xxxx",
# #         "dbpassword": "xxxx",
# #         "dbhost": "xxxxxxx",
# #         "dbport": 3306,
# #         "dbname": "mldb"
# #     }
#
#
# # 连接redis配置
# RedisCfg = {
#     "startup_nodes_jd": [
#         {"host": "127.0.0.1", "port": 6379}],  # 嘉定
#     "startup_nodes_wgq": [
#         {"host": "127.0.0.1", "port": 6379},  # 外高桥
#     ],
#     "pass_wd": r""
# }
#
# # RedisCfg = {
# #     "startup_nodes_jd": [
# #         {"host": "xxxxxx", "port": 6379}],  # 嘉定
# #     "startup_nodes_wgq": [
# #         {"host": "xxxxxx", "port": 6379},  # 外高桥
# #     ],
# #     "pass_wd": r"Oper1234"
# # }
#
#
# # 数据库基础配置表
# TableConfig = {
#     "redisacq_table": "redis_acq_config",
#     "total_1m_table": "grjr_flink1m_3d",
#     "total_map_table": "grjr_flink1m_3d",
#     "total_switch_user": "grjr_user",
#     "total_switch_data": "grjr_cmc"
# }