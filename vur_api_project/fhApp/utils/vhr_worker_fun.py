# -*- coding: utf-8 -*-
import warnings
import json
import time
import random
from kafka import KafkaProducer
from ..utils.constants import MESSAGEID_TO_NAME


warnings.filterwarnings("ignore")


# 2.1 vhr--mock数据生成器
class DataGenerator:
    def __init__(self, bootstrap_servers='121.36.73.252:30085', topic='twg'):  # 李少隐
        # def __init__(self, bootstrap_servers='39.107.107.149:9092', topic='twg'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)

    def generate_data(self, userId, vin, messageId, flag):

        name = random.choice(MESSAGEID_TO_NAME[messageId])
        # print(name)

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
                "value": random.randint(100, 10000) if flag == '1' else 0,  # 值  ?????????
                "unit": "",  # 单位
                "timestamp": int(time.time() * 1000),  # 根据flag判断改为异常还是正常
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


