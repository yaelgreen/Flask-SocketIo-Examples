import os

SECRET_KEY = 'justasecretkeythatishouldputhere'
REDIS_URL = os.environ.get("REDIS_URL", '127.0.0.1')
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
MESSAGE_RECEIVED_SIGNAL = 10
NUMBER_OF_SECONDS_FOR_TIMER = 10
CHANNEL = "event fired"
