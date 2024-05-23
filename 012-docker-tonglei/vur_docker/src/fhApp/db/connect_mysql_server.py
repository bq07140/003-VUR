# # coding:utf-8
# """
#     @author:"XT2/DC/ICBC"
#     @file:connect_mysql_server.py
# """
# import logging
#
# import pymysql
#
# # from perFinan.config import DatabaseConfig
# from .db_config import DatabaseConfig
#
#
# class MysqlConn(object):
#     def __init__(self, host=DatabaseConfig["dbhost"], user=DatabaseConfig["dbuser"],
#                  passwd=DatabaseConfig["dbpassword"], db=DatabaseConfig["dbname"],
#                  port=DatabaseConfig["dbport"], charset='utf8', cursorclass=pymysql.cursors.DictCursor):
#         try:
#             self.conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset=charset,
#                                         cursorclass=cursorclass)
#             self.cursor = self.conn.cursor()
#         except Exception as e:
#             logging.error(e)
#             raise ConnectionError
#
#     def get_all(self, sql, param=None):
#         if param is None:
#             count = self.cursor.execute(sql)
#         else:
#             count = self.cursor.execute(sql, param)
#         if count > 0:
#             result = self.cursor.fetchall()
#         else:
#             result = None
#         return result
#
#     def get_one(self, sql, param=None):
#         if param is None:
#             count = self.cursor.execute(sql)
#         else:
#             count = self.cursor.execute(sql, param)
#         if count > 0:
#             result = self.cursor.fetchone()
#         else:
#             result = None
#         return result
#
#     def update(self, sql, param=None):
#         if param is None:
#             result = self.cursor.execute(sql)
#         else:
#             result = self.cursor.execute(sql, param)
#         return result
#
#     def insert_one(self, sql, value):
#         result = self.cursor.execute(sql, value)
#         self.conn.commit()
#         return result
#
#     def insert_one_no_param(self, sql):
#         result = self.cursor.execute(sql)
#         self.conn.commit()
#         return result
#
#     def insert_many(self, sql, values):
#         count = self.cursor.executemany(sql, values)
#         self.conn.commit()
#         return count
#
#     def delete(self, sql, param=None):
#         if param is None:
#             count = self.cursor.execute(sql)
#         else:
#             count = self.cursor.execute(sql, param)
#         return count
#
#     def dispose(self, is_end=1):
#         try:
#             if is_end == 1:
#                 self.conn.commit()
#             else:
#                 self.cursor.rollback()
#             self.cursor.close()
#             self.conn.close()
#         except Ellipsis:
#             return False
#
#
