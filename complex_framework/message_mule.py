import json
import uwsgi
from redis import Redis

from config import REDIS_URL, REDIS_PORT, \
    MESSAGE_RECEIVED_SIGNAL, CHANNEL


def local_mule_task(**kwargs):
    """
    A function called once an event is received
    Args:
        **kwargs: the data passed with the received message
    """
    print(f'local mule task executed with {kwargs}')


def receive_messages():
    """
    A mule service to listen to events sent on redis channel CHANNEL
    """
    client = Redis(REDIS_URL, REDIS_PORT)
    info = client.info("server")
    redis_version_streams = False
    if 'redis_version' in info and int(
            info['redis_version'].split('.')[0]) >= 5:
        redis_version_streams = True

    if redis_version_streams and hasattr(client, 'xread'):
        ID = "$"
        while True:
            message = client.xread({CHANNEL: ID}, None, 0)
            # WSGI signaling to notify all workers
            uwsgi.signal(MESSAGE_RECEIVED_SIGNAL)
            ID = message[0][1][0][0]
    else:
        pubsub = client.pubsub()
        pubsub.subscribe(CHANNEL)

        for message in pubsub.listen():
            # WSGI signaling to notify all workers
            uwsgi.signal(MESSAGE_RECEIVED_SIGNAL)
            if isinstance(message, dict) and 'data' in message and isinstance(
                    message['data'], bytes):
                message_data = json.loads(message['data'])
                local_mule_task(**message_data)


if __name__ == '__main__':
    receive_messages()
