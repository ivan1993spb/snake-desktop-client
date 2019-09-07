from sys import argv
from websocket import create_connection
import json
from lib.handlers import MessageRootHandler, MessageBroadcastHandler, MessageGameHandler, MessagePlayerHandler
from lib.playground import Playground
import logging


logging.basicConfig(level=logging.DEBUG)

group = "1"

if len(argv) > 1:
    group = argv[1]

url = "ws://localhost:8080/ws/games/{}".format(group)
print(url)

ws = create_connection(url)


h = MessageRootHandler(
    MessageGameHandler(Playground()),
    MessagePlayerHandler(),
    MessageBroadcastHandler(),
)


while True:
    try:
        result = ws.recv()
        message = json.loads(result)
        h.handle(message)
    except KeyboardInterrupt:
        break

ws.close()

