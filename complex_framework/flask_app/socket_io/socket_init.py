from flask_socketio import SocketIO

from config import REDIS_URL, REDIS_PORT
from flask_app.socket_io.socket_events import SocketEvents


def init_socket(app):

    redis_server_url = app.config.get('REDIS_URL', REDIS_URL)
    redis_server_port = app.config.get('REDIS_PORT', REDIS_PORT)

    socket = SocketIO(app, async_mode='gevent_uwsgi', message_queue=f'redis://{redis_server_url}:'
                                         f'{redis_server_port}')

    socket.on_namespace(SocketEvents('/events'))
    return socket
