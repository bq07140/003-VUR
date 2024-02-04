"""
    python脚本，每秒钟，从 INDICATORS_LI 列表中抽一条指标数据存入 kafka，
    最终存入 dts_test 表中
"""
import json
import time
import random
from kafka import KafkaProducer


# 1. 各种指标mock数据列表
INDICATORS_VUR = [

    # # 1.1 横向加速度
    # {
    #     "name": "EML_BeschlX_XIX_EML_06_XIX_E3V_ABCANFD",
    #     "value": random.choice([-3, 0, 3]),  # round(random.uniform(-20.45, 20.45), 2)
    #     "unit": "m/s*2"
    # },

    # 1.2 纵向加速度
    {
        "name": "EML_BeschlY_XIX_EML_06_XIX_E3V_ABCANFD",
        "value": random.choice([-1, 0, 0, 3]),  # round(random.uniform(-20.45, 20.45), 2) 大于0.3
        "unit": "m/s*2"
    },
    # 1.3 速度
    {
        "name": "EML_GeschwX_XIX_EML_06_XIX_E3V_FASCANFD1",
        "value": round(random.uniform(200, 500), 2),   # 实际 (0, 127.8125)
        "unit": "m/s"
    },

    # =========================
    # 2.1 转向角度
    {
        "name": "EML_Gierwinkel_XIX_EML_06_XIX_E3V_FASCANFD2",
        "value": round(random.uniform(-3.14, 3.14), 2),
        "unit": "rad"
    },
    # 2.2 打方向盘速度  LWI_Lenkradw_Geschw
    {
        "name": "LWI_Lenkradw_Geschw_XIX_LWI_01_XIX_E3V_ACANFD",
        "value": round(random.uniform(-2500, 2500), 2),
        "unit": "Grad/s"
    },

    # # =========================
    # # 3.1 ACC正在启动===
    # {
    #     "name": "ACC_Anfahren_XIX_ACC_18_XIX_E3V_FASCANFD1",
    #     "value": random.choice([0 for i in range(4)] + [1]),  # 原始数据   [0, 1]
    #     "unit": ""
    # },

    # # =========================
    # # 4.1 驾驶统计
    # {
    #     "name": "someip_drivingstatistics_1_3.0_field_distances_notifier_49184",
    #     "value": round(random.uniform(0.7, 1.5), 2),  # 实际为 (0,500)
    #     "unit": "km"
    # },

    # =========================
    # 5.1 能耗
    {
        "name": "someip_electricalconsumptions_1_3.0_field_averageConsumptions_notifier_49168",
        "value": round(random.uniform(10, 350), 2),  # 原始 (0, 35)
        "unit": "L"
    },

    # # =========================
    # # 6.1 直流充电
    # {
    #     "name": "BMS_DC_Ladeprofil_Wechsel_XIX_BMS_26_XIX_E3V_EVCANFD",
    #     "value": random.choice([0 for i in range(4)] + [1]),  #  [0, 1]
    #     "unit": ""
    # },

    # # 6.2 实时电量 (上升判断开始充电)
    # {
    #     "name": "BMS_Ladezustand_XIX_BMS_22_XIX_E3V_EVCANFD",
    #     "value": random.randint(0, 100),
    #     "unit": ""
    # },
    # # 6.3 开始充电===
    # {
    #     "name": "BMS_IstModus_XIX_BMS_20_XIX_E3V_EVCANFD",
    #     "value": random.choice([0 for i in range(4)] + [1]),  # 原始 4= AC Charing ; 6= DC Charging  [4, 6]
    #     "unit": ""
    # },

    # 2.  =======================  第二批指标  =====================
    # 冷却液01
    {
        "name": "BCM_Kuehlmittel_Sensor_XIX_BCM_01_XIX_E3V_KCAN",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # 冷却液02
    {
        "name": "BCM_Kuehlmittel_Sensor_02_XIX_BCM_01_XIX_E3V_KCAN",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # 雨刮水
    {
        "name": "Wischer_vorne_defekt_XIX_Wischer_01_XIX_E3V_KCAN",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # 制动盘04
    {
        "name": "BCM_Bremsbelag_Sensor_NAR_XIX_SAM_01_XIX_E3V_KCAN",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # 制动盘03
    {
        "name": "BCM_Bremsbelag_Sensor_XIX_BCM_01_XIX_E3V_KCAN",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # 制动盘02
    {
        "name": "BCM_Bremsbelag_Sensor_Rdw_XIX_SAM_01_XIX_E3V_KCAN",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # 制动盘01
    {
        "name": "BCM_Bremsbelag_Sensor_CND_XIX_SAM_01_XIX_E3V_KCAN",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # 盲区检测
    {
        "name": "ACC_Blindheit_erkannt_XIX_ACC_18_XIX_E3V_ACANFD",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # Ecall
    {
        "name": "EA_eCall_Anf_XIX_EA_04_XIX_HCP4_CANFD03",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # Bcall
    {
        "name": "bCall_active_XIX_TM_01_XIX_E3V_FASCANFD1",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # # Icall  --暂时取消
    # {
    #     "name": "iCall_active_XIX_TM_01_XIX_E3V_K2CANFD",
    #     "value": random.choice([0, random.randint(100, 10000)]),
    #     "unit": ""
    # },
    # 自动除雾
    {
        "name": "FSH_Status_XIX_Klima_16_XIX_E3V_EVCANFD",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # 充放电电压04
    {
        "name": "BMS_RtmWarnUZelleMin_XIX_BMS_28_XIX_E3V_EVCANFD",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # 充放电电压03
    {
        "name": "BMS_RtmWarnUZelleMax_XIX_BMS_28_XIX_E3V_EVCANFD",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # 充放电电压02
    {
        "name": "BMS_RtmWarnUPackMin_XIX_BMS_28_XIX_E3V_EVCANFD",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # 充放电电压01
    {
        "name": "BMS_RtmWarnUPackMax_XIX_BMS_28_XIX_E3V_EVCANFD",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # 电池管理
    {
        "name": "BMS_RtmWarnZelleZustand_XIX_BMS_28_XIX_E3V_EVCANFD",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # 绝缘电阻
    {
        "name": "BMS_IsoFehler_XIX_BMS_11_XIX_E3V_ACANFD",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # 电池温度03
    {
        "name": "BMS_RtmWarnTZelleMin_XIX_BMS_28_XIX_E3V_EVCANFD",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # 电池温度02
    {
        "name": "BMS_RtmWarnTZelleMax_XIX_BMS_28_XIX_E3V_EVCANFD",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # 电池温度01
    {
        "name": "BMS_RtmWarnTZelleDiff_XIX_BMS_28_XIX_E3V_EVCANFD",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
    # 电池碰撞/进水检测
    {
        "name": "BMS_Fehler_Notabschaltung_Crash_XIX_BMS_20_XIX_E3V_EVCANFD",
        "value": random.choice([0, random.randint(100, 10000)]),
        "unit": ""
    },
]


# 2. mock数据生成器
class DataGenerator(object):

    def __init__(self, bootstrap_servers='121.36.73.252:30085', topic='twg002'):  # 李少隐
    # def __init__(self, bootstrap_servers='39.107.107.149:9092', topic='twg'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)

    def generate_data(self):

        indicator = random.choice(INDICATORS_VUR)
        # print(indicator)
        # print(indicator['name'])

        data_li = []

        user_vin = random.choice([
            {
                "userId": "393b4915-8a1a-43c9-a5e1-2710057fdf8b",
                "vehicleId": "b9487cfbc0c74499a970d5d08d2878c1",
            },
            {
                "userId": "17362fa4-6e13-41b2-866d-f27553296e4e",
                "vehicleId": "46e7e2f9ef3845628ea2bb8738fb6f51",
            },
            {
                "userId": "7f3b3811-f732-426b-a65f-095cb4046b12",
                "vehicleId": "LAVTDMERZAA000050",
            },
            {
                "userId": "3a8e9f6d-bbd5-41dc-ba1d-c1cb6468001c",
                "vehicleId": "LAVTDMERZAA000050",
            }
        ])

        timestamp = int(time.time() * 1000)

        data = {
            "userId": user_vin['userId'],
            "vehicleId": user_vin['vehicleId'],
            "schemaId": "Schema-363a2145-3c28-41cb-9255-806722709cee",
            "userMessageId": "FUM-1153",
            "useCaseIds": ["UseCase-1f8fc8bb-a824-46d3-972a-8492da542b4a"],
            "time": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "payload": {
                "mdc_id": 180940,
                "g_id": 1,
                "name": indicator['name'],  # 指标名称
                "value": indicator['value'],  # 值
                "unit": indicator['unit'],  # 单位
                "timestamp": timestamp,
                "containerMsgId": 4,
                "orderId": "5a7dada3-5a54-4d21-8c9a-7061cf3599b3",
                "containerId": "6d5a9a65-ed4e-4524-9690-23df17473a4b",
                "containerMsgCount": 4,
                "ingest_timestamp": int(time.time() * 1000),
                "orderVersion": 0,
                "correlationId": ""
            }
        }
        data_li.append(data)

        return data_li

    def connect_kafka(self):
        producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
        return producer

    def send_to_kafka(self, data):
        try:
            json_data = json.dumps(data).encode('utf-8')
            self.producer.send(self.topic, json_data)
            print("Message sent successfully")
        except Exception as e:
            print(f"Error: {e}")

    def main(self):
        try:
            # while True:
            for i in range(5):  # 每次发送5条数据
                data_li = self.generate_data()
                for data in data_li:
                    self.send_to_kafka(data)
                    time.sleep(1)

        finally:
            self.producer.close()


if __name__ == "__main__":
    data_generator = DataGenerator()
    data_generator.main()





