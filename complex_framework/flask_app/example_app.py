from flask import Flask, render_template
from flask_socketio import emit
from uwsgidecorators import timer, signal
import datetime as dt
from flask_cors import CORS

from config import NUMBER_OF_SECONDS_FOR_TIMER, MESSAGE_RECEIVED_SIGNAL
from flask_app.pubsub_client import PubSubClient
from flask_app.socket_io.socket_init import init_socket
from gevent import monkey

monkey.patch_all()


app = Flask(__name__)
app.config.from_pyfile('../config.py')


socketio = init_socket(app)
CORS(app)


@timer(NUMBER_OF_SECONDS_FOR_TIMER, target='mule')
def publish_event(signum):
    """
    Publish event using redis pub \ sub client from any service.
    Decorated with uwsgi timer, it will run every NUMBER_OF_SECONDS_FOR_TIMER
    Args:
        signum: The number for the signal
    """
    message = {
        'status': 'fire event',
        'time': dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    }
    print(f"publish event via redis client: {message}")
    client = PubSubClient(
        app.config['REDIS_URL'],
        app.config['REDIS_PORT'])
    client.send_event_fired_message(message)


@app.route('/')
def index():
    """
    Render and return a response for the index page
    Returns:
        Index page
    """
    return render_template('index.html')


@socketio.on('connect')
def on_connect():
    """
    Notify all clients once the socket.io is connected
    """
    print("socket.io connected")
    payload = dict(data='Connected')
    emit('log', payload, broadcast=True)


@signal(MESSAGE_RECEIVED_SIGNAL)
def receive_signal(signum: int):
    """
    Decorated with uwsgi signal, this will run each time a signal
    MESSAGE_RECEIVED_SIGNAL is fired.
    Receive the signal, log it, and notify all clients
    Args:
        signum: The number for the signal
    """
    msg = f"received signal on signal number {signum}"
    print(msg)
    socketio.emit('log', dict(data=msg), broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
