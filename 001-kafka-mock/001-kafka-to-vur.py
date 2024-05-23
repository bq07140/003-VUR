from confluent_kafka import Consumer, KafkaError, KafkaException

conf = {
    'bootstrap.servers': 'kafka-pub.prod.dts.vwautocloud.cn:33350',
    'group.id': 'my_consumer_group',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'SCRAM-SHA-256',
    'sasl.username': 'megatrontui',
    'sasl.password': 'megatrontui',
    'ssl.endpoint.identification.algorithm': 'https',
    'ssl.ca.location': './_ssl/client.truststore.jks',
    'ssl.key.location': './_ssl/client.keystore.jks',
    'ssl.key.password': 'key123456',
    'ssl.certificate.location': './_ssl/client.keystore.jks'
}

c = Consumer(conf)

c.subscribe(['DDS-MEGATRON_VHR_CORE_PROD'])

try:
    while True:
        msg = c.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition, the message is consumed when all messages
                # in a partition have been consumed.
                print('%% %s [%d] reached end at offset %d\n' %
                      (msg.topic(), msg.partition(), msg.offset()))
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            print('Received message: {}'.format(msg.value().decode('utf-8')))
except KeyboardInterrupt:
    pass

finally:
    # Clean up on exit
    c.close()
