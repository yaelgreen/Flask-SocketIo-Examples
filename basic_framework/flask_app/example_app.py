from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'justasecretkeythatishouldputhere'

socket_io = SocketIO(app)
CORS(app)


@app.route('/')
def index():
    """
    Render and return a response for the index page
    Returns:
        Index page
    """
    return render_template('index.html')


@app.route('/api')
def api():
    """
    Send to all clients on socket.io the data received in the request args
    Returns:
        A json indicating the success
    """
    query = dict(request.args)
    socket_io.emit('log', dict(data=str(query)), broadcast=True)
    return jsonify(dict(success=True, message='Received'))


@socket_io.on('connect')
def on_connect():
    """
    Notify all clients once the socket.io is connected
    """
    payload = dict(data='Connected')
    emit('log', payload, broadcast=True)


if __name__ == '__main__':
    socket_io.run(app)
