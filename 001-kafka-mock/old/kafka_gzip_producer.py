from kafka import KafkaProducer
import json

# 创建Kafka生产者
producer = KafkaProducer(
    bootstrap_servers='121.36.73.252:30085',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),  # 序列化消息为JSON格式
    compression_type='gzip'  # 启用gzip压缩
)

# 生产者发送消息
topic = 'twg_gzip'
for i in range(100):
    message = {'key': 'gzip test ...222'}
    producer.send(topic, value=message)

# 关闭生产者
producer.close()


