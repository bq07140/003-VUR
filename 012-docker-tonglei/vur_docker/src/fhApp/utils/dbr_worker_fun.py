# -*- coding: utf-8 -*-
import warnings
import json
import time
import random
from flask import g
from datetime import datetime
from kafka import KafkaProducer
from ..utils.constants import MESSAGEID_LI
# from databricks import sql
import mysql.connector

warnings.filterwarnings("ignore")


class QueryDatabricks(object):

    def __init__(self):
        # # self.conn = g.db_pool.connection()  # 1. 连接池
        # # 2. 单连接
        # self.conn = sql.connect(
        #     server_hostname="adb-2515004071041721.1.databricks.azure.cn",
        #     http_path="/sql/1.0/warehouses/07194f39c23cde02",
        #     access_token="dapideac683303ce305bcf4971b955c39bbf")
        #
        # self.cursor = self.conn.cursor()
        self.warning_lights = []

        self.aggr_dbr_monthly_table = "aggr_dbr_monthly"
        self.aggr_dbr__daily_table = "aggr_dbr__daily"
        self.gdc_vhr_tb = "gdc_vhr_tb"

        # 3. 连接Azure mysql
        self.conn = mysql.connector.connect(
            user="tanwg",
            password="pass@1234",
            host="vur-python-mysql.mysql.database.chinacloudapi.cn",
            port=3306,
            database="vur_db",
            # ssl_ca="{ca-cert filename}",
            # ssl_disabled=False,
        )

        # 4. 使用连接创建游标对象
        self.cursor = self.conn.cursor(dictionary=True)

    # def __del__(self):
    def close_db(self):
        self.cursor.close()
        self.conn.close()

    def timestamp_to_str(self, timestamp):

        dt_object = datetime.utcfromtimestamp(timestamp)
        formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')

        return formatted_time

    # def aggr_dbr_monthly(self, month_id, page, num):
    #
    #     try:
    #         sql = """
    #                 SELECT userId,vin,month_id,acceleration_cnt,deceleration_cnt,sharp_turn_cnt,
    #                        acc_activate_cnt,mileage,low_charging_cnt,high_charging_cnt,charging_cnt,
    #                        ROUND(electrical_consumptions, 2) as electrical_consumptions,
    #                        month_date
    #                 from {0}
    #                 where month_id='{1}'
    #                 order by month_id desc,userId,vin;
    #               """.format(self.aggr_dbr_monthly_table, month_id)
    #         # print(sql)
    #
    #         self.cursor.execute(sql)
    #         ret = self.cursor.fetchall()
    #
    #     except Exception as e:
    #         print(str(e))
    #
    #     return ret

    def aggr_dbr_monthly(self, month_id, page, num):

        try:
            sql = """
                    SELECT userId,vin,month_id,acceleration_cnt,deceleration_cnt,sharp_turn_cnt, 
                           acc_activate_cnt,mileage,low_charging_cnt,high_charging_cnt,charging_cnt, 
                           ROUND(electrical_consumptions, 2) as electrical_consumptions,
                           month_date 
                    FROM {0} 
                    WHERE month_id='{1}'
                    ORDER BY month_id DESC, userId, vin
                    LIMIT {2} OFFSET {3};
                  """.format(self.aggr_dbr_monthly_table, month_id, num, (page - 1) * num)

            total_sql = """
                            SELECT COUNT(*) totalnum
                            FROM {0} 
                            WHERE month_id='{1}';
                        """.format(self.aggr_dbr_monthly_table, month_id)

            self.cursor.execute(sql)
            ret = self.cursor.fetchall()

            self.cursor.execute(total_sql)
            totalnum = self.cursor.fetchone()['totalnum']
            totalpage = totalnum // num + (1 if totalnum % num > 0 else 0)

        except Exception as e:
            print(str(e))
            ret = []
            totalnum = 0
            totalpage = 0

        return ret, totalnum, totalpage

    def aggr_dbr_daily(self, day_id, page, num):

        try:
            sql = """
                    SELECT userId,vin,day_id,acceleration_cnt,deceleration_cnt,sharp_turn_cnt, 
                           acc_activate_cnt,mileage,low_charging_cnt,high_charging_cnt,charging_cnt, 
                           ROUND(electrical_consumptions, 2) as electrical_consumptions,
                           report_date 
                    from {0} 
                    where day_id='{1}' and mileage>200
                    order by day_id desc,userId,vin
                    LIMIT {2} OFFSET {3};;
                  """.format(self.aggr_dbr__daily_table, day_id, num, (page - 1) * num)
            # print(sql)

            total_sql = """
                           SELECT COUNT(*) totalnum
                           FROM {0} 
                           WHERE day_id='{1}';
                       """.format(self.aggr_dbr__daily_table, day_id)

            self.cursor.execute(sql)
            ret = self.cursor.fetchall()
            self.cursor.execute(total_sql)
            totalnum = self.cursor.fetchone()['totalnum']
            totalpage = totalnum // num + (1 if totalnum % num > 0 else 0)

        except Exception as e:
            print(str(e))
            ret = []
            totalnum = 0
            totalpage = 0

        return ret, totalnum, totalpage

    def vdaa_gdc(self, vin):
        data = {}
        try:
            # 1. 先根据vin，从redis查，
            data_str = g.db_redis.get_name_value(vin)
            # print(data_str, type(data_str))

            # 2. redis有，就从redis返回。
            if data_str:
                data_str = data_str.replace("'", '"')
                data = json.loads(data_str)
                # print(ret, type(ret))

            # 3. redis没有，就从hive查询，然后保存到redis。
            else:
                sql = """
                        SELECT userId, vehicleId, name, status, timestamp, date_id
                        FROM (
                            SELECT userId, vehicleId, name, status, timestamp, date_id,
                                   ROW_NUMBER() OVER (PARTITION BY name
                                   ORDER BY timestamp DESC) as row_num
                            FROM {0}
                            WHERE vehicleId='{1}' and status=1
                        ) as aaa
                        WHERE aaa.row_num=1;
                      """.format(self.gdc_vhr_tb, vin)
                # print(sql)

                sql_maxtime = """
                            SELECT max(timestamp) maxtime
                            FROM {0}
                            WHERE vehicleId='{1}' 
                      """.format(self.gdc_vhr_tb, vin)
                # print(sql_maxtime)
                self.cursor.execute(sql_maxtime)
                ret_maxtime = self.cursor.fetchall()
                # print(ret_maxtime)

                if ret_maxtime:
                    data['lastReceivedTimes'] = ret_maxtime[0].get('maxtime').strftime("%Y-%m-%d %H:%M:%S")
                else:
                    data['lastReceivedTimes'] = ""

                self.cursor.execute(sql)
                ret = self.cursor.fetchall()
                # print(ret)

                if ret:
                    for line in ret:
                        timestamp_str = line.get('timestamp').strftime("%Y-%m-%d %H:%M:%S")
                        name = line.get('name')

                        self.warning_lights.append(
                            {
                                "warningLightTextCn": MESSAGEID_LI[name]['warningLightTextCn'],
                                "warningLightTextEn": MESSAGEID_LI[name]['warningLightTextEn'],
                                "iconColor": "Yellow",
                                "messageId": name,
                                "timeOfOccurrence": timestamp_str
                            }
                        )

                    data['warningLights'] = self.warning_lights

                    print(data)
                    # print(type(data))
                    # print(str(data))
                    # print(type(str(data)))
                    # # 3.2 设置到redis中
                    # g.db_redis.setex(vin, 5, str(data))
                    print('------------11111111111111111')
                    # g.db_redis.setex(vin, 20, 'tanwengang')

                else:
                    data['warningLights'] = []
                    data['lastReceivedTimes'] = ""

        except Exception as e:
            print(str(e))
            data['warningLights'] = []
            data['lastReceivedTimes'] = ""
        return data


# 2.2 DBR--mock数据生成器
class DbrDataGenerator:
    def __init__(self, bootstrap_servers='121.36.73.252:30085', topic='twg'):  # 李少隐
        # def __init__(self, bootstrap_servers='39.107.107.149:9092', topic='twg'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)

    def connect_kafka(self):
        producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
        return producer

    def send_to_kafka(self, data):
        try:
            # print(data)
            json_data = json.dumps(data).encode('utf-8')
            self.producer.send(self.topic, json_data)
            print("Msg sent successfully")
        except Exception as e:
            print(f"Error: {e}")

    def get_timestamp(self, day_id):
        current_time_microseconds = datetime.now().strftime('%H:%M:%S.%f')

        complete_datetime_str = f'{day_id} {current_time_microseconds[:-3]}'  # 去除微秒中的最后三位，保留毫秒

        # 将日期时间字符串转换为日期时间对象
        date_time_object = datetime.strptime(complete_datetime_str, '%Y-%m-%d %H:%M:%S.%f')
        print(date_time_object)

        # 将日期时间对象转换为时间戳（精确到毫秒）
        timestamp_milliseconds = date_time_object.timestamp() * 1000
        print("指定日期+当前时分秒的时间戳（精确到毫秒）:", timestamp_milliseconds)

        return timestamp_milliseconds

    # 1. 通用函数
    def dbr_general_send_fun(self, userId, vin, name, timestamp):

        data = {
            "userId": userId,
            "vehicleId": vin,
            "schemaId": "Schema-363a2145-3c28-41cb-9255-806722709cee",
            "userMessageId": "FUM-1153",
            "useCaseIds": ["UseCase-1f8fc8bb-a824-46d3-972a-8492da542b4a"],
            "time": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "payload": {
                "mdc_id": 180940,
                "g_id": 1,
                "name": name,  # 指标名称
                "value": 1,  # 值  ?????????
                "unit": "times",  # 单位
                "timestamp": timestamp,
                "containerMsgId": 4,
                "orderId": "5a7dada3-5a54-4d21-8c9a-7061cf3599b3",
                "containerId": "6d5a9a65-ed4e-4524-9690-23df17473a4b",
                "containerMsgCount": 4,
                "ingest_timestamp": timestamp,
                "orderVersion": 0,
                "correlationId": ""
            }
        }
        return [data]

    # 2. 低充次数
    def low_charging(self, userId, vin, name, timestamp):

        # 2.1 充电信号
        data = {
            "userId": userId,
            "vehicleId": vin,
            "schemaId": "Schema-363a2145-3c28-41cb-9255-806722709cee",
            "userMessageId": "FUM-1153",
            "useCaseIds": ["UseCase-1f8fc8bb-a824-46d3-972a-8492da542b4a"],
            "time": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "payload": {
                "mdc_id": 180940,
                "g_id": 1,
                "name": name,  # 指标名称
                "value": 1,  # 值
                "unit": "times",  # 单位
                "timestamp": timestamp,
                "containerMsgId": 4,
                "orderId": "5a7dada3-5a54-4d21-8c9a-7061cf3599b3",
                "containerId": "6d5a9a65-ed4e-4524-9690-23df17473a4b",
                "containerMsgCount": 4,
                "ingest_timestamp": timestamp,
                "orderVersion": 0,
                "correlationId": ""
            }
        }

        # 2.2 电量信号
        current_charge_name = "BMS_Ladezustand_XIX_BMS_22_XIX_E3V_EVCANFD"

        current_charge_data = {
            "userId": userId,
            "vehicleId": vin,
            "schemaId": "Schema-363a2145-3c28-41cb-9255-806722709cee",
            "userMessageId": "FUM-1153",
            "useCaseIds": ["UseCase-1f8fc8bb-a824-46d3-972a-8492da542b4a"],
            "time": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "payload": {
                "mdc_id": 180940,
                "g_id": 1,
                "name": current_charge_name,  # 指标名称
                "value": random.randint(0, 9),  # 值
                "unit": "times",  # 单位
                "timestamp": timestamp,
                "containerMsgId": 4,
                "orderId": "5a7dada3-5a54-4d21-8c9a-7061cf3599b3",
                "containerId": "6d5a9a65-ed4e-4524-9690-23df17473a4b",
                "containerMsgCount": 4,
                "ingest_timestamp": timestamp,
                "orderVersion": 0,
                "correlationId": ""
            }
        }

        return [data, current_charge_data]

    # 3. 高充次数
    def high_charging(self, userId, vin, name, timestamp):

        # 2.1 充电信号
        data = {
            "userId": userId,
            "vehicleId": vin,
            "schemaId": "Schema-363a2145-3c28-41cb-9255-806722709cee",
            "userMessageId": "FUM-1153",
            "useCaseIds": ["UseCase-1f8fc8bb-a824-46d3-972a-8492da542b4a"],
            "time": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "payload": {
                "mdc_id": 180940,
                "g_id": 1,
                "name": name,  # 指标名称
                "value": 1,  # 值
                "unit": "times",  # 单位
                "timestamp": timestamp,
                "containerMsgId": 4,
                "orderId": "5a7dada3-5a54-4d21-8c9a-7061cf3599b3",
                "containerId": "6d5a9a65-ed4e-4524-9690-23df17473a4b",
                "containerMsgCount": 4,
                "ingest_timestamp": timestamp,
                "orderVersion": 0,
                "correlationId": ""
            }
        }

        # 2.2 电量信号
        current_charge_name = "BMS_Ladezustand_XIX_BMS_22_XIX_E3V_EVCANFD"

        current_charge_data = {
            "userId": userId,
            "vehicleId": vin,
            "schemaId": "Schema-363a2145-3c28-41cb-9255-806722709cee",
            "userMessageId": "FUM-1153",
            "useCaseIds": ["UseCase-1f8fc8bb-a824-46d3-972a-8492da542b4a"],
            "time": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "payload": {
                "mdc_id": 180940,
                "g_id": 1,
                "name": current_charge_name,  # 指标名称
                "value": random.randint(96, 100),  # 值
                "unit": "times",  # 单位
                "timestamp": timestamp,
                "containerMsgId": 4,
                "orderId": "5a7dada3-5a54-4d21-8c9a-7061cf3599b3",
                "containerId": "6d5a9a65-ed4e-4524-9690-23df17473a4b",
                "containerMsgCount": 4,
                "ingest_timestamp": timestamp,
                "orderVersion": 0,
                "correlationId": ""
            }
        }

        return [data, current_charge_data]

    # 4. 里程函数
    def mileage(self, userId, vin, name, timestamp):

        data = {
            "userId": userId,
            "vehicleId": vin,
            "schemaId": "Schema-363a2145-3c28-41cb-9255-806722709cee",
            "userMessageId": "FUM-1153",
            "useCaseIds": ["UseCase-1f8fc8bb-a824-46d3-972a-8492da542b4a"],
            "time": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "payload": {
                "mdc_id": 180940,
                "g_id": 1,
                "name": name,  # 指标名称
                "value": 20,  # 值
                "unit": "km",  # 单位
                "timestamp": timestamp,
                "containerMsgId": 4,
                "orderId": "5a7dada3-5a54-4d21-8c9a-7061cf3599b3",
                "containerId": "6d5a9a65-ed4e-4524-9690-23df17473a4b",
                "containerMsgCount": 4,
                "ingest_timestamp": timestamp,
                "orderVersion": 0,
                "correlationId": ""
            }
        }
        return [data]











