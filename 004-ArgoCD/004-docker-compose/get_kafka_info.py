from kafka import KafkaAdminClient, KafkaConsumer

# 设置Kafka集群的地址（多个地址以逗号分隔）
# bootstrap_servers = '119.96.173.17:9092,kafka_broker2:9092,kafka_broker3:9092'  # 替换为实际的Kafka broker地址
# bootstrap_servers = '119.96.173.17:9092'  # 替换为实际的Kafka broker地址
bootstrap_servers = '39.107.107.149:9092'  # 替换为实际的Kafka broker地址

# 使用KafkaAdminClient来获取集群信息
admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
cluster_info = admin_client.describe_cluster()

# 使用KafkaConsumer来获取集群的topic列表
consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
topics = consumer.topics()

# 打印集群信息和topic列表
print("Kafka集群信息:")
print(cluster_info)
print("\nKafka集群中的Topic列表:")
print(topics)

# 判断Kafka是单机还是集群
if len(cluster_info['brokers']) > 1:
    print("\nKafka是一个集群。")
else:
    print("\nKafka是单机模式。")






