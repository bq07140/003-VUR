"""
    python脚本，每秒钟，从 INDICATORS_LI 列表中抽一条指标数据存入 kafka，
    最终存入 dts_test 表中
"""
import json
import time
from kafka import KafkaProducer


# 2. mock数据生成器
class DataGenerator:

    def __init__(self, bootstrap_servers='121.36.73.252:30085', topic='twg'):
    # def __init__(self, bootstrap_servers='39.107.107.149:9092', topic='tdr001'):
    # def __init__(self, bootstrap_servers='39.99.143.169:9092', topic='twg'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)

    def generate_data(self):

        data = {
                "userId": "393b4915-8a1a-43c9-a5e1-2710057fdf8b",
                "vehicleId": "b9487cfbc0c74499a970d5d08d2878c1",
                "schemaId": "Schema-363a2145-3c28-41cb-9255-806722709cee",
                "userMessageId": "FUM-1153",
                }
        return data

    def send_to_kafka(self, data):
        try:
            json_data = json.dumps(data).encode('utf-8')
            self.producer.send(self.topic, json_data)
            print("Message sent successfully")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    data_g = DataGenerator()

    while True:
        # for i in range(5000):
        data = data_g.generate_data()
        print(data)
        data_g.send_to_kafka(data)
        time.sleep(1)
