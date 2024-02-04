from confluent_kafka import Consumer, KafkaError

# Kafka集群的地址
bootstrap_servers = '39.107.107.149:9092'
# 主题名称
topic = 'test'
# 分区编号
partition = 0
# 消费者组ID
group_id = 'your_consumer_group'

# 配置消费者
conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest'  # 从最早的消息开始消费
}

# 创建消费者
consumer = Consumer(conf)

# 订阅指定的主题和分区
consumer.subscribe([f'{topic}'])
# consumer.subscribe([f'{topic}:{partition}'])

try:
    while True:
        # 从主题中获取消息
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            # 处理错误消息
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # 消费到分区末尾，继续下一轮消费
                continue
            else:
                # 其他错误，打印错误信息
                print(msg.error())
                break

        # 处理消息
        print(f"Consumed message: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    # 用户按下Ctrl + C，退出消费者程序
    pass

finally:
    # 关闭消费者
    consumer.close()
