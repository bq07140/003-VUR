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
    # 1.21 是否充电
    {
        "name": "isCharging",
        "value": random.choice([0, 1]),
        "unit": "cm"
    },
    # 1.20 IPA泊车距离，单位:厘米
    {
        "name": "parkingIPADistance",
        "value": random.randint(30, 150),
        "unit": "cm"
    },
    # 1.19 IPA泊车时间，单位秒
    {
        "name": "parkingIPADuration",
        "value": random.randint(30, 150),
        "unit": "s"
    },
    # 1.18 IPA泊车次数
    {
        "name": "parkingIPATimes",
        "value": random.randint(2, 6),
        "unit": ""
    },
    # 1.17 记忆泊车距离，单位:厘米
    {
        "name": "rememberParkingDistance",
        "value": random.randint(50, 200),
        "unit": "cm"
    },
    # 1.16 记忆泊车时间，单位秒
    {
        "name": "rememberParkingDuration",
        "value": random.randint(30, 600),
        "unit": "s"
    },
    # 1.15 记忆泊车次数
    {
        "name": "rememberParkingTimes",
        "value": random.randint(2, 6),
        "unit": ""
    },
    # 1.14 车辆能耗
    {
        "name": "carPowerConsumption",
        "value": round(random.uniform(15, 35), 2),
        "unit": ""
    },
    # 1.13 驾驶时间(单位min，scrm传过来的开始和结束时间，就是驾驶时间)
    {
        "name": "drivingDuration",
        "value": random.randint(50, 200),
        "unit": "min"
    },
    # 1.12 转弯打死行驶次数
    {
        "name": "turningCornerTimes",
        "value": random.randint(5, 10),
        "unit": ""
    },
    # 1.11 Travel Assist工作百分比
    {
        "name": "travelAssistWorkPercent",
        "value": round(random.uniform(0.2, 1), 2),
        "unit": "h"
    },
    # 1.10 Travel Assist工作时长
    {
        "name": "travelAssistWorkDuration",
        "value": round(random.uniform(1, 5), 2),
        "unit": "h"
    },
    # 1.9 Assist工作次数
    {
        "name": "travelAssistWorkTimes",
        "value": random.randint(1, 5),
        "unit": ""
    },
    # 1.8 ESP次数
    {
        "name": "espTimes",
        "value": random.randint(5, 30),
        "unit": ""
    },
    # 1.7 加速次数
    {
        "name": "absTimes",
        "value": random.randint(5, 30),
        "unit": ""
    },
    # 1.6 行驶里程
    {
        "name": "traveledMileage",
        "value": round(random.uniform(50, 200), 2),
        "unit": "km"
    },
    # 1.5 结束时续航里程
    {
        "name": "endMileage",
        "value": round(random.uniform(150, 200), 2),
        "unit": "km"
    },
    # 1.4 开始时续航里程
    {
        "name": "startMileage",
        "value": round(random.uniform(300, 400), 2),
        "unit": "km"
    },
    # 1.3 加速次数
    {
        "name": "accelerateTimes",
        "value": random.randint(5, 30),
        "unit": ""
    },
    # 1.2 最高时速
    {
        "name": "maxSpeed",
        "value": round(random.uniform(100, 127), 2),
        "unit": "km/h"
    },
    # 1.1 平均时速
    {
        "name": "avgSpeed",
        "value": round(random.uniform(60, 80), 2),
        "unit": "km/h"
    },
]


# 2. mock数据生成器
class DataGenerator(object):

    def __init__(self, bootstrap_servers='119.96.173.17:9092', topic='tdr002'):  # 赵存伟老师的kafka
    # def __init__(self, bootstrap_servers='119.96.173.17:9092', topic='tdr'):  # 赵存伟老师的kafka
    # def __init__(self, bootstrap_servers='39.107.107.149:9092', topic='tdr'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)

    def generate_data(self):

        indicator = random.choice(INDICATORS_VUR)
        print(indicator)

        user_vin = random.choice([
            {
                "userId": "393b4915-8a1a-43c9-a5e1-2710057fdf8b",
                "vehicleId": "b9487cfbc0c74499a970d5d08d2878c1",
            },
            {
                "userId": "17362fa4-6e13-41b2-866d-f27553296e4e",
                "vehicleId": "46e7e2f9ef3845628ea2bb8738fb6f51",
            }
        ])

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
            json_data = json.dumps(data).encode('utf-8')
            self.producer.send(self.topic, json_data)
            print("Message sent successfully")
        except Exception as e:
            print(f"Error: {e}")

    def main(self):
        try:
            while True:
            # for i in range(5000):
                data = self.generate_data()
                # print(data)
                self.send_to_kafka(data)
                time.sleep(1)

        finally:
            self.producer.close()


if __name__ == "__main__":
    data_generator = DataGenerator()
    data_generator.main()






