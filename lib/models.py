
import random
from functools import partial
from num2words import num2words


class Game:
    GAME_NAME_PREFIX = "Game"

    def __init__(self, id_, limit, count, width, height, rate):
        self.id = id_
        self.limit = limit
        self.count = count
        self.width = width
        self.height = height
        self.rate = rate

    @property
    def number(self):
        return self.id

    @property
    def name(self):
        return '{} {}'.format(self.GAME_NAME_PREFIX, num2words(self.number))

    def deletable(self):
        return self.count == 0

    @classmethod
    def from_json_dict(cls, dct):
        return Game(id_=dct['id'],
                    limit=dct['limit'],
                    count=dct['count'],
                    width=dct['width'],
                    height=dct['height'],
                    rate=dct['rate'])


_RAND_GAME_INT_FROM = 0
_RAND_GAME_INT_TO = 100

_rand_value = partial(random.randint, _RAND_GAME_INT_FROM, _RAND_GAME_INT_TO)


def rand_game() -> Game:
    return Game(
        id_=_rand_value(),
        count=_rand_value(),
        limit=_rand_value(),
        width=_rand_value(),
        height=_rand_value(),
        rate=_rand_value(),
    )


def zero_game() -> Game:
    return Game(id_=0, count=0, limit=0, width=0, height=0, rate=0)


class Server:
    def __init__(self, name, address, secured_scheme=False):
        self.__name = name
        self.__address = address
        self.__secured_scheme = secured_scheme

    @property
    def api(self):
        return "{}://{}/api".format('https' if self.__secured_scheme else 'http', self.__address)

    @property
    def websocket(self):
        return '{}://{}/ws'.format('wss' if self.__secured_scheme else 'ws', self.__address)

    def to_yaml_dict(self):
        return {
            'name': self.__name,
            'address': self.__address,
            'secured_scheme': self.__secured_scheme,
        }

    @classmethod
    def from_yaml_dict(cls, dct):
        return Server(**dct)

    @property
    def name(self):
        return self.__name

    @property
    def address(self):
        return self.__address

    @property
    def secured_scheme(self):
        return self.__secured_scheme


def local_server():
    return Server('Local', 'localhost:8080', False)
