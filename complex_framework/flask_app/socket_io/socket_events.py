import logging

from flask_socketio import Namespace


class SocketEvents(Namespace):

    logger = logging.getLogger(__name__)

    def on_connect(self):
        self.logger.debug(f"New consumer connected to the socket")

