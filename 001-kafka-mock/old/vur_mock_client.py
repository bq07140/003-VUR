from kafka import KafkaProducer


def test_kafka_connection(broker):
    try:
        producer = KafkaProducer(bootstrap_servers=[broker], api_version=(0, 10))
        print("Connection to Kafka broker successful.")
        producer.close()
    except Exception as e:
        print(f"Failed to connect to Kafka broker: {e}")


# 测试Kafka连接
# kafka_broker = "kafka.tui.dts.vwautocloud.cn:32750"
kafka_broker = "kafka-pub.tui.dts.vwautocloud.cn:32750"
test_kafka_connection(kafka_broker)



