# """
#     @author:"XT2/DC/ICBC"
#     @file:check_redis.py
#     @time:2021/9/1 16:28
# """
# import logging
# import datetime
#
# import pymysql
#
# # check_sql_cfg = \
# #     {
# #         "dbuser": "stdb",
# #         "dbpassword": "Oper1234",
# #         "dbhost": "76.7.50.118",
# #         "dbport": 3306,
# #         "dbname": "hope3"\\
# #     }
# check_sql_cfg = {
#     "dbuser": "stdb",
#     "dbpassword": "KTxt@123",
#     "dbhost": "84.10.93.69",
#     "dbport": 3306,
#     "dbname": "hope3"
# }
# check_table = "redischeck"
# model_name = "个人金融"
# default_area = "jd"
# backup_area = "wgq"
# time_span = 600
#
#
# def get_redis_version():
#     area_list = list()
#     now_time = datetime.datetime.now().replace(microsecond=0)
#     try:
#         # 创建数据库的链接
#         conn = pymysql.connect(host=check_sql_cfg["dbhost"], user=check_sql_cfg["dbuser"],
#                                passwd=check_sql_cfg["dbpassword"], db=check_sql_cfg["dbname"], charset='utf8',
#                                cursorclass=pymysql.cursors.DictCursor, connect_timeout=0.1)
#         with conn.cursor() as cursor:
#             sql = "SELECT redisgroup,status,checktime from {table} where modulename = '{modulename}'" \
#                   "".format(table=check_table, modulename=model_name)
#             count = cursor.execute(sql)
#             if count > 0:
#                 res = cursor.fetchall()
#                 for data in res:
#                     # 探活的状态是OK
#                     if data.get("status") == "OK":
#                         # 检查探测时间和系统时间的秒差值
#                         time_total = (now_time - data.get("checktime")).total_seconds()
#                         if 0 <= time_total <= time_span:
#                             area_list.append(data.get("redisgroup").lower())
#             else:
#                 res = None
#         conn.close()
#     except Exception as e:
#         logging.error(e)
#         res = None
#     if res:
#         if area_list:
#             if default_area in area_list:
#                 # 返回默认地区
#                 return default_area
#             else:
#                 # 返回备份地区
#                 return backup_area
#         else:
#             return default_area
#     else:
#         return default_area
