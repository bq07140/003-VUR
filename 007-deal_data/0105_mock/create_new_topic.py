from kafka import KafkaAdminClient
from kafka.admin import NewTopic

# Kafka 服务器地址和端口
bootstrap_servers = '121.36.73.252:30085'

# 新主题的名称
new_topic_name = 'twg002'

# 新主题的分区数量
new_partitions = 3

admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

# 构建 NewTopic 对象
new_topic = NewTopic(
    name=new_topic_name,
    num_partitions=new_partitions,
    replication_factor=1  # 设置副本因子，这里设置为 1
)

# 创建新主题
admin_client.create_topics(new_topics=[new_topic])

# 关闭 AdminClient
admin_client.close()
