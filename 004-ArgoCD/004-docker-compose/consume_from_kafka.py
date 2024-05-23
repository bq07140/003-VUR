from kafka import KafkaConsumer
import json

# bootstrap_servers = '39.99.143.169:9092'
# bootstrap_servers = '39.107.107.149:9092'
bootstrap_servers = '121.36.73.252:30085'

topic = 'twg'
# topic = 'tdr001'

group_id = 'my_group_id'

consumer = KafkaConsumer(topic,
                         group_id=group_id,
                         bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')))

for message in consumer:
    data = message.value
    print("Received message:", data)




