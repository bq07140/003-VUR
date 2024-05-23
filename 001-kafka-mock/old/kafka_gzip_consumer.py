from kafka import KafkaConsumer
import json

# 创建Kafka消费者
consumer = KafkaConsumer(
    'twg_gzip',
    bootstrap_servers='121.36.73.252:30085',
    auto_offset_reset='latest',  # 设置偏移量重置策略  latest  earliest
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # 反序列化消息
)

# 消费者订阅主题并拉取消息
for message in consumer:
    print("Received message:", message.value)

# 关闭消费者
consumer.close()
