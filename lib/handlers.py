import logging
from lib.playground import Playground


logger = logging.getLogger(__name__)


class MessageInvalidTypeError(Exception):

    def __init__(self, t):
        super().__init__('Invalid message type: {}'.format(t))


class MessageGameInvalidTypeError(Exception):

    def __init__(self, t):
        super().__init__('Invalid message game type: {}'.format(t))


class MessagePlayerInvalidTypeError(Exception):

    def __init__(self, t):
        super().__init__('Invalid message player type: {}'.format(t))


class MessageGameHandler:

    MESSAGE_GAME_FIELD_TYPE = 'type'
    MESSAGE_GAME_FIELD_PAYLOAD = 'payload'

    MESSAGE_GAME_TYPE_ERROR = 'error'
    MESSAGE_GAME_TYPE_CREATE = 'create'
    MESSAGE_GAME_TYPE_DELETE = 'delete'
    MESSAGE_GAME_TYPE_UPDATE = 'update'
    MESSAGE_GAME_TYPE_CHECKED = 'checked'

    # These events occur on a playground:
    HANDLE_EVENT_PLAYGROUND = (MESSAGE_GAME_TYPE_CREATE,
                               MESSAGE_GAME_TYPE_UPDATE,
                               MESSAGE_GAME_TYPE_DELETE,
                               MESSAGE_GAME_TYPE_CHECKED)

    def __init__(self, pg: Playground):
        self._pg = pg

    def handle(self, message: dict):
        if message[self.MESSAGE_GAME_FIELD_TYPE] in self.HANDLE_EVENT_PLAYGROUND:
            self._pg.handle(message)
        elif message[self.MESSAGE_GAME_FIELD_TYPE] == self.MESSAGE_GAME_TYPE_ERROR:
            logger.info("An error message has been received: %s", message)
        else:
            raise MessageGameInvalidTypeError(message[self.MESSAGE_GAME_FIELD_TYPE])

    def _update(self):
        pass


class MessagePlayerHandler:

    MESSAGE_PLAYER_FIELD_TYPE = 'type'
    MESSAGE_PLAYER_FIELD_PAYLOAD = 'payload'

    MESSAGE_PLAYER_TYPE_SIZE = 'size'
    MESSAGE_PLAYER_TYPE_SNAKE = 'snake'
    MESSAGE_PLAYER_TYPE_NOTICE = 'notice'
    MESSAGE_PLAYER_TYPE_ERROR = 'error'
    MESSAGE_PLAYER_TYPE_COUNTDOWN = 'countdown'
    MESSAGE_PLAYER_TYPE_OBJECTS = 'objects'

    def __init__(self):
        pass

    def handle(self, message):
        if message[self.MESSAGE_PLAYER_FIELD_TYPE] == self.MESSAGE_PLAYER_TYPE_SIZE:
            pass
        elif message[self.MESSAGE_PLAYER_FIELD_TYPE] == self.MESSAGE_PLAYER_TYPE_SNAKE:
            pass
        elif message[self.MESSAGE_PLAYER_FIELD_TYPE] == self.MESSAGE_PLAYER_TYPE_NOTICE:
            pass
        elif message[self.MESSAGE_PLAYER_FIELD_TYPE] == self.MESSAGE_PLAYER_TYPE_ERROR:
            pass
        elif message[self.MESSAGE_PLAYER_FIELD_TYPE] == self.MESSAGE_PLAYER_TYPE_COUNTDOWN:
            pass
        elif message[self.MESSAGE_PLAYER_FIELD_TYPE] == self.MESSAGE_PLAYER_TYPE_OBJECTS:
            pass
        else:
            raise MessagePlayerInvalidTypeError(message[self.MESSAGE_PLAYER_FIELD_TYPE])


class MessageBroadcastHandler:

    def __init__(self):
        pass

    def handle(self, message):
        logger.info('Received broadcast message: %s', message)


class MessageRootHandler:

    MESSAGE_FIELD_TYPE = 'type'
    MESSAGE_FIELD_PAYLOAD = 'payload'

    MESSAGE_TYPE_GAME = 'game'
    MESSAGE_TYPE_PLAYER = 'player'
    MESSAGE_TYPE_BROADCAST = 'broadcast'

    def __init__(self,
                 game_handler: MessageGameHandler,
                 player_handler: MessagePlayerHandler,
                 broadcast_handler: MessageBroadcastHandler):
        self._player_handler = player_handler
        self._game_handler = game_handler
        self._broadcast_handler = broadcast_handler

    def handle(self, message):
        logger.debug('Handle message: %s', message)

        if message[self.MESSAGE_FIELD_TYPE] == self.MESSAGE_TYPE_GAME:
            self._game_handler.handle(message[self.MESSAGE_FIELD_PAYLOAD])
        elif message[self.MESSAGE_FIELD_TYPE] == self.MESSAGE_TYPE_PLAYER:
            self._player_handler.handle(message[self.MESSAGE_FIELD_PAYLOAD])
        elif message[self.MESSAGE_FIELD_TYPE] == self.MESSAGE_TYPE_BROADCAST:
            self._broadcast_handler.handle(message[self.MESSAGE_FIELD_PAYLOAD])
        else:
            raise MessageInvalidTypeError(message[self.MESSAGE_FIELD_TYPE])
