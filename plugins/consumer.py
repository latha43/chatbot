from kafka import KafkaConsumer

consumer = KafkaConsumer('add_user_topic')

for message in consumer:
    print(message.key,message.value)


