from flask import Flask, jsonify, request
from databricks import sql
import logging
import pandas as pd
import json
import datetime

logging.getLogger("insert_to_ods_gdc_daily.py").setLevel(logging.DEBUG)
logging.basicConfig(filename="insert_to_ods_gdc_daily.log", level=logging.ERROR)

app = Flask(__name__)


class QueryDatabricks(object):

    def __init__(self):
        self.conn = sql.connect(
            server_hostname="adb-2515004071041721.1.databricks.azure.cn",
            http_path="/sql/1.0/warehouses/07194f39c23cde02",
            access_token="dapi9aefab090c8d18b7619235656a43b0ef")

        self.cursor = self.conn.cursor()
        self.yesterday = datetime.date.today() - datetime.timedelta(days=1)
        self.data = []

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def insert_pd(self, ret_df):

        # 将DataFrame转换为指定的列表格式
        result_list = ret_df.apply(lambda row: (row['userId'], row['vehicleId'],
                                                row['name'], row['value'], row['timestamp']), axis=1).tolist()

        values = ",".join([f"({a}, {b}, {c}, {d}, {e})" for (a, b, c, d, e) in result_list])

        ret = self.cursor.execute(f"INSERT INTO hive_metastore.default.ods_gdc_daily (userId, vehicleId, name, value, timestamp) VALUES {values}")
        print(ret)

    def query_dts_test(self):

        try:
            sql = """
                    SELECT * from hive_metastore.default.dts_test limit 5000;
                  """
            # print(sql)

            self.cursor.execute(sql)
            ret = self.cursor.fetchall()

            ret = [json.loads(line.asDict()['value']) for line in ret]

            new_ret = [{
                        'userId': i.get('userId'),
                        'vehicleId': i.get('vehicleId'),
                        'name': i.get('payload').get('name'),
                        'value': i.get('payload').get('value'),
                        'timestamp': i.get('payload').get('timestamp'),
                        } for i in ret]

            df = pd.DataFrame(new_ret)

            # 将timestamp列转换为日期时间对象
            df['timestamp'] = (df['timestamp'] / 1000).astype(int)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

            # 获取昨天的日期
            yesterday = datetime.date.today() - datetime.timedelta(days=1)

            # 筛选出timestamp为昨天的所有数据
            filtered_df = df[df['timestamp'].dt.date == yesterday]

            # 将日期时间对象转换为以秒为单位的时间戳
            ret_df = filtered_df.copy()
            ret_df['timestamp'] = ret_df['timestamp'].apply(lambda x: x.timestamp())
            print(ret_df)

            self.insert_pd(ret_df)

        except Exception as e:
            print(str(e))


if __name__ == '__main__':

    databricks = QueryDatabricks()
    ret = databricks.query_dts_test()






