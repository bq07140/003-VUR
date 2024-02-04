import json
import time
import random
import logging
from flask import Flask, jsonify, request
from databricks import sql
from datetime import datetime
from kafka import KafkaProducer

logging.getLogger("response_aggr_dbr_api.py").setLevel(logging.DEBUG)
logging.basicConfig(filename="../response_aggr_dbr_api.log", level=logging.ERROR)

app = Flask(__name__)

# 建一张配置表  messageId  name  warningLightTextCn  warningLightTextEn  unit

# 告警配置信息
MESSAGEID_LI = {
    "battery_temp": {
        "warningLightTextCn": "故障：电池温度",
        "warningLightTextEn": "Error: Please check battery temperature!",
    },
    "insulation_resist": {
        "warningLightTextCn": "故障：绝缘电阻",
        "warningLightTextEn": "Error: Please check insulation resist!",
    },
    "battery_collision_waterDetect": {
        "warningLightTextCn": "故障：电池碰撞/进水检测",
        "warningLightTextEn": "Error: Please check battery collision or waterDetect!",
    },
    "battery_management": {
        "warningLightTextCn": "故障：电池管理",
        "warningLightTextEn": "Error: Please check battery management!",
    },
    "charging_discharging_voltage": {
        "warningLightTextCn": "故障：充放电电压",
        "warningLightTextEn": "Error: Please check charing and discharging voltage!",
    },
    "automatic_defog": {
        "warningLightTextCn": "故障：自动除雾",
        "warningLightTextEn": "Error: Please check automatic defog!",
    },
    "b_call": {
        "warningLightTextCn": "故障：Bcall",  # 紧急呼叫
        "warningLightTextEn": "Error: Please check Bcall!",
    },
    "e_call": {
        "warningLightTextCn": "故障：Ecall",  # 紧急呼叫
        "warningLightTextEn": "Error: Please check Ecall!",
    },
    "blind_spot_detect": {
        "warningLightTextCn": "故障：盲区检测",
        "warningLightTextEn": "Error: Please check blind spot detect!",
    },
    "brake_disc": {
        "warningLightTextCn": "故障：制动盘",
        "warningLightTextEn": "Error: Please check brake disc!",
    },
    "wiper_water": {
        "warningLightTextCn": "故障：雨刮水",
        "warningLightTextEn": "Error: Please check wiper water!",
    },
    "coolant": {
        "warningLightTextCn": "故障：冷却液",
        "warningLightTextEn": "Error: Please check coolant!",
    },
}


# messageId --- 指标名称的映射
MESSAGEID_TO_NAME = {
    # 电池温度
    "battery_temp": ["BMS_RtmWarnTZelleDiff_XIX_BMS_28_XIX_E3V_EVCANFD",
                     "BMS_RtmWarnTZelleMax_XIX_BMS_28_XIX_E3V_EVCANFD",
                     "BMS_RtmWarnTZelleMin_XIX_BMS_28_XIX_E3V_EVCANFD"],
    # 绝缘电阻
    "insulation_resist": ["BMS_IsoFehler_XIX_BMS_11_XIX_E3V_ACANFD"],
    # 电池碰撞/进水检测
    "battery_collision_waterDetect": ["BMS_Fehler_Notabschaltung_Crash_XIX_BMS_20_XIX_E3V_EVCANFD"],
    # 电池管理
    "battery_management": ["BMS_RtmWarnZelleZustand_XIX_BMS_28_XIX_E3V_EVCANFD"],
    # 充放电电压
    "charging_discharging_voltage": ["BMS_RtmWarnUPackMax_XIX_BMS_28_XIX_E3V_EVCANFD",
                                     "BMS_RtmWarnUPackMin_XIX_BMS_28_XIX_E3V_EVCANFD",
                                     "BMS_RtmWarnUZelleMax_XIX_BMS_28_XIX_E3V_EVCANFD",
                                     "BMS_RtmWarnUZelleMin_XIX_BMS_28_XIX_E3V_EVCANFD"],
    # 自动除雾
    "automatic_defog": ["FSH_Status_XIX_Klima_16_XIX_E3V_EVCANFD"],
    "b_call": ["bCall_active_XIX_TM_01_XIX_E3V_FASCANFD1"],
    "e_call": ["EA_eCall_Anf_XIX_EA_04_XIX_HCP4_CANFD03"],
    # "i_call": ["iCall_active_XIX_TM_01_XIX_E3V_K2CANFD"],  # 暂时不用
    # 盲区检测
    "blind_spot_detect": ["ACC_Blindheit_erkannt_XIX_ACC_18_XIX_E3V_ACANFD"],
    # 制动盘
    "brake_disc": ["BCM_Bremsbelag_Sensor_CND_XIX_SAM_01_XIX_E3V_KCAN",
                   "BCM_Bremsbelag_Sensor_Rdw_XIX_SAM_01_XIX_E3V_KCAN",
                   "BCM_Bremsbelag_Sensor_XIX_BCM_01_XIX_E3V_KCAN",
                   "BCM_Bremsbelag_Sensor_NAR_XIX_SAM_01_XIX_E3V_KCAN"],
    # 雨刮水
    "wiper_water": ["Wischer_vorne_defekt_XIX_Wischer_01_XIX_E3V_KCAN"],
    # 冷却液
    "coolant": ["BCM_Kuehlmittel_Sensor_XIX_BCM_01_XIX_E3V_KCAN",
                "BCM_Kuehlmittel_Sensor_02_XIX_BCM_01_XIX_E3V_KCAN"],
}


# 2. mock数据生成器
class DataGenerator:
    # def __init__(self, bootstrap_servers='39.107.107.149:9092', topic='twg'):
    def __init__(self, bootstrap_servers='119.96.173.17:9092', topic='zcw'):  # 赵存伟老师的kafka
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)

    def generate_data(self, userId, vin, messageId):

        # messageId --- name
        name = random.choice(MESSAGEID_TO_NAME[messageId])
        print(name)

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
                "value": random.randint(100, 10000),  # 值
                "unit": "",  # 单位
                "timestamp": int(time.time() * 1000),
                "containerMsgId": 4,
                "orderId": "5a7dada3-5a54-4d21-8c9a-7061cf3599b3",
                "containerId": "6d5a9a65-ed4e-4524-9690-23df17473a4b",
                "containerMsgCount": 4,
                "ingest_timestamp": int(time.time() * 1000),
                "orderVersion": 0,
                "correlationId": ""
            }
        }
        return data

    def connect_kafka(self):
        producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
        return producer

    def send_to_kafka(self, data):
        try:
            # print(data)
            json_data = json.dumps(data).encode('utf-8')
            self.producer.send(self.topic, json_data)
            print("Message sent successfully")
        except Exception as e:
            print(f"Error: {e}")


class QueryDatabricks(object):

    def __init__(self):
        self.conn = sql.connect(
            server_hostname="adb-2515004071041721.1.databricks.azure.cn",
            http_path="/sql/1.0/warehouses/07194f39c23cde02",
            access_token="dapi27116197bf3636c59422a74de3e768ab")

        self.cursor = self.conn.cursor()
        self.warning_lights = []

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def timestamp_to_str(self, timestamp):

        dt_object = datetime.utcfromtimestamp(timestamp)
        formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')

        return formatted_time

    def aggr_dbr_monthly(self, month_start, month_end):

        try:
            sql = """
                    SELECT userId,vin,month_id,acceleration_cnt,deceleration_cnt,sharp_turn_cnt, 
                           acc_activate_cnt,mileage,low_charging_cnt,high_charging_cnt,charging_cnt, 
                           ROUND(electrical_consumptions, 2) as electrical_consumptions,
                           month_date 
                    from hive_metastore.default.aggr_dbr_monthly 
                    where month_id>='{0}' and month_id<='{1}'
                    order by month_id desc,userId,vin;
                  """.format(month_start, month_end)
            # print(sql)

            self.cursor.execute(sql)
            ret = self.cursor.fetchall()
            ret = [line.asDict() for line in ret]

        except Exception as e:
            print(str(e))

        return ret

    def aggr_dbr_daily(self, day_start, day_end):

        try:
            sql = """
                    SELECT userId,vin,day_id,acceleration_cnt,deceleration_cnt,sharp_turn_cnt, 
                           acc_activate_cnt,mileage,low_charging_cnt,high_charging_cnt,charging_cnt, 
                           ROUND(electrical_consumptions, 2) as electrical_consumptions,
                           report_date 
                    from hive_metastore.default.aggr_dbr__daily 
                    where day_id>='{0}' and day_id<='{1}'and mileage>200
                    order by day_id desc,userId,vin;
                  """.format(day_start, day_end)
            # print(sql)

            self.cursor.execute(sql)
            ret = self.cursor.fetchall()
            ret = [line.asDict() for line in ret]

        except Exception as e:
            print(str(e))

        return ret

    def vdaa_gdc(self, userId, vin):

        try:

            sql = """
                    SELECT userId, vehicleId, name, status, timestamp, date_id
                    FROM (
                        SELECT userId, vehicleId, name, status, timestamp, date_id,
                               ROW_NUMBER() OVER (PARTITION BY userId, vehicleId,
                               name ORDER BY timestamp DESC) as row_num
                        FROM hive_metastore.default.vdaa_gdc_v2_read
                        WHERE userId='{0}' AND vehicleId='{1}'
                    )
                    WHERE row_num=1;
                  """.format(userId, vin)

            # print(sql)

            # import time
            # time_st = time.time()

            self.cursor.execute(sql)

            # print(time.time() - time_st)

            ret = self.cursor.fetchall()

            ret = [line.asDict() for line in ret]

            if ret:
                for line in ret:
                    timestamp_str = line.get('timestamp').strftime("%Y-%m-%d %H:%M:%S")
                    status = line.get('status')
                    name = line.get('name')

                    if status != 0:
                        self.warning_lights.append(
                            {
                                "warningLightTextCn": MESSAGEID_LI[name]['warningLightTextCn'],
                                "warningLightTextEn": MESSAGEID_LI[name]['warningLightTextEn'],
                                "iconColor": "Yellow",
                                "messageId": name,
                                "timeOfOccurrence": timestamp_str
                            }
                        )

                    else:
                        self.warning_lights.append(
                            {
                                "warningLightTextCn": "",
                                "warningLightTextEn": "",
                                "iconColor": "",
                                "messageId": name,
                                "timeOfOccurrence": timestamp_str
                            }
                        )

                ret = self.warning_lights

        except Exception as e:
            print(str(e))
            ret = []
        return ret


# http://127.0.0.1:5000/aggr_dbr_monthly?month_start=2023-10&month_end=2023-11
@app.route('/aggr_dbr_monthly')
def aggr_dbr_monthly():
    month_start = request.args.get('month_start')
    month_end = request.args.get('month_end')

    response = {
        'code': 200,
        'msg': 'Success',
        'data': []
    }

    if all([month_start, month_end]):
        try:
            databricks = QueryDatabricks()
            ret = databricks.aggr_dbr_monthly(month_start, month_end)
            response['data'] = ret

        except Exception as e:
            logging.error(str(e))
            response['code'] = 500
            response['msg'] = str(e)

    else:
        msg = 'Bad Request: Missing required parameters'
        response['code'] = 400
        response['msg'] = msg
        logging.error(msg)

    return jsonify(response)


# http://127.0.0.1:5000/aggr_dbr_daily?day_start=2023-11-06&day_end=2023-11-08
@app.route('/aggr_dbr_daily')
def aggr_dbr_daily():
    day_start = request.args.get('day_start')
    day_end = request.args.get('day_end')

    response = {
        'code': 200,
        'msg': 'Success',
        'data': []
    }

    if all([day_start, day_end]):

        try:
            databricks = QueryDatabricks()
            ret = databricks.aggr_dbr_daily(day_start, day_end)
            response['data'] = ret

        except Exception as e:
            logging.error(str(e))
            response['code'] = 500
            response['msg'] = str(e)

    else:
        msg = 'Bad Request: Missing required parameters'
        response['code'] = 400
        response['msg'] = msg
        logging.error(msg)

    return jsonify(response)


# http://127.0.0.1:5000/produce_one_mock_data?userId=393b4915-8a1a-43c9-a5e1-2710057fdf8b&vin=b9487cfbc0c74499a970d5d08d2878c1&messageId=battery_temp
@app.route('/produce_one_mock_data')
def produce_one_mock_data():
    userId = request.args.get('userId')
    vin = request.args.get('vin')
    messageId = request.args.get('messageId')

    response = {
        'code': 200,
        'msg': 'Success',
        'data': ""
    }

    if all([userId, vin, messageId]):

        try:
            # 给kafka发送一条数据
            data_generator = DataGenerator()

            try:
                data = data_generator.generate_data(userId, vin, messageId)
                data_generator.send_to_kafka(data)
                ret = "%s : message sent successfully" % messageId
            except Exception as e:
                print(str(e))
                ret = str(e)

            data_generator.producer.close()

            response['data'] = ret

        except Exception as e:
            logging.error(str(e))
            response['code'] = 500
            response['msg'] = str(e)

    else:
        msg = 'Bad Request: Missing required parameters'
        response['code'] = 400
        response['msg'] = msg
        logging.error(msg)

    return jsonify(response)


# http://127.0.0.1:5000/vdaa_gdc?userId=393b4915-8a1a-43c9-a5e1-2710057fdf8b&vin=b9487cfbc0c74499a970d5d08d2878c1
@app.route('/vdaa_gdc')
def vdaa_gdc():

    userId = request.args.get('userId')
    vin = request.args.get('vin')

    response = {
        'code': 200,
        'msg': 'Success',
        'data': {}
    }

    if all([userId, vin]):

        try:
            databricks = QueryDatabricks()
            ret = databricks.vdaa_gdc(userId, vin)
            response['data']['warningLights'] = ret

            # response['data']['warningLights'] = []

        except Exception as e:
            logging.error(str(e))
            response['code'] = 500
            response['msg'] = str(e)

    else:
        msg = 'Bad Request: Missing required parameters'
        response['code'] = 400
        response['msg'] = msg
        logging.error(msg)

    return jsonify(response)


if __name__ == '__main__':
    # print(app.url_map)
    app.run(host='0.0.0.0', debug=True)









