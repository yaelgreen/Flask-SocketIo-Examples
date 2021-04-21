import redis
import json

from config import CHANNEL


class PubSubClient:
    """
    A Pub Sub redis client

    Args:
        _client (Redis): A Redis instance,
            initialized with a redis server host and port.

    Attributes:
        _client (Redis): A Redis instance,
            initialized with a redis host and port.

    """

    _client = None

    def __init__(self, redis_host: str, redis_port: int):
        self._client = redis.Redis(redis_host, redis_port)

    def send_event_fired_message(self, data: dict):
        """
        Send a message on the channel CHANNEL
        Args:
            data: the message to send
        """
        self.send_message(data, CHANNEL)

    def send_message(self, message: dict, channel: str):
        """
        Send a message on the channel
        Args:
            message: the message to send
            channel: the channel to send the message on
        """
        info = self._client.info("server")
        if not hasattr(self._client, 'xadd') or ('redis_version' in info and
                                                 int(info['redis_version'].split('.')[0]) < 5):
            message_json = json.dumps(message)
            self._client.publish(channel, message_json)
        else:
            self._client.xadd(channel, message)
