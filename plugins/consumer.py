import json
from kafka import KafkaConsumer
import datetime
import time

consumer = KafkaConsumer('chat-bot-topic-devops', bootstrap_servers='localhost:9092',
                        value_deserializer=lambda m: json.loads(m))
for msg in consumer:
    data = msg.value
    print(msg.key)
    print(data) 