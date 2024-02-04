# openssl pkcs7 -print_certs -in megatron.kafka.tui.dts.vwautocloud.cn.p7b -out megatron.kafka.tui.dts.vwautocloud.cn.pem
# 这将从 P7B 文件中提取证书，并将其保存为 PEM 格式的文件 `megatron.kafka.tui.dts.vwautocloud.cn.pem`。

from kafka import KafkaConsumer

# SSL 相关配置
ssl_cafile = "./megatron.kafka.tui.dts.vwautocloud.cn.pem"  # PEM 格式证书文件路径

# Kafka broker 地址
bootstrap_servers = "kafka.tui.dts.vwautocloud.cn:32750"
# bootstrap_servers = "kafka-pub.tui.dts.vwautocloud.cn:32750"

# 创建 KafkaConsumer 实例
consumer = KafkaConsumer(
    "DDS-MEGATRON_RD_CORE_TUI",
    bootstrap_servers=bootstrap_servers,
    api_version=(0, 10),
    security_protocol="SSL",
    ssl_cafile=ssl_cafile,
)

# 持续消费数据
print('--------11111')
for message in consumer:
    print(f"Received message: {message.value.decode()}")

# 关闭 KafkaConsumer
consumer.close()





