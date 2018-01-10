import json
from kafka import KafkaProducer
from rtmbot.core import Plugin
import datetime


class DevopsPlugin(Plugin):
    topic = 'chat-bot-topic-devops'

    allowed_tokens = [
        'git', 'hi', 'hello', 'good', 'morning', 'evening',
        'svn', 'add', 'user', 'project', 'repo', 'permission'
    ]

    @classmethod
    def _is_command_allowed(cls, text):
        # returns tokens which are not in the allowed tokens
        command = set(text.split(' ')[0].replace('!', ''))
        return len(set(command) - set(cls.allowed_tokens)) == 0

    def ingest(self, key, value):
        value['ts'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%s')
        producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        producer.send(self.topic, key=key, value=value)
        producer.flush()
        producer.close()
