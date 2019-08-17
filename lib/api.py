from concurrent.futures import Future
from requests.utils import CaseInsensitiveDict
import requests.exceptions
import requests
from requests_futures.sessions import FuturesSession


class APIError(Exception):
    pass


class APIClient(FuturesSession):
    USER_AGENT_DEFAULT = 'SnakeAPIClient'
    POOL_SIZE = 4

    def __init__(self, entrypoint: str, user_agent=None):
        if not entrypoint.endswith('api'):
            raise APIError('API entrypoint has to end with suffix "api"')

        super().__init__(max_workers=self.POOL_SIZE)
        self._entrypoint = entrypoint
        self._user_agent = user_agent if user_agent else self.USER_AGENT_DEFAULT

        self.headers.update(self.__initial_headers())

    def __initial_headers(self):
        return CaseInsensitiveDict({
            'User-Agent': self._user_agent,
            'X-Snake-Client': self._user_agent,
            'Accept': 'application/json',
        })

    def get_games(self):
        return self._call('GET', self._compose_url('games'))

    def get_game(self, game_id: int):
        return self._call('GET', self._compose_url('games', str(game_id)))

    def get_game_objects(self, game_id: int):
        return self._call('GET', self._compose_url('games', str(game_id), 'objects'))

    def delete_game(self, game_id: int):
        return self._call('DELETE', self._compose_url('games', str(game_id)))

    def create_game(self, limit: int, width: int, height: int):
        return self._call('POST', self._compose_url('games'), data={
            'limit': limit,
            'width': width,
            'height': height,
        })

    def broadcast(self, game_id: int, message: str):
        return self._call('POST', self._compose_url('games', str(game_id), 'broadcast'), data={
            'message': message,
        })

    def capacity(self):
        return self._call('GET', self._compose_url('capacity'))

    def info(self):
        return self._call('GET', self._compose_url('info'))

    def ping(self):
        return self._call('GET', self._compose_url('ping'))

    def _compose_url(self, *argv):
        return '/'.join((self._entrypoint,) + argv)

    def _call(self, method: str, url: str, data=None):
        future = self.request(method.upper(), url, data=data)
        return APIResponse(future)


class APIResponse:
    FIELD_ERROR_TEXT = 'text'
    EMPTY_ERROR_TEXT = 'empty error text'

    def __init__(self, future: Future):
        self._data = None
        self._status_code = 0
        self._future = future

    @property
    def error_msg(self):
        if not self._future.done():
            return None

        if self._status_code in [200, 201]:
            return None

        if isinstance(self._data, dict):
            return self._data.get(self.FIELD_ERROR_TEXT, self.EMPTY_ERROR_TEXT)

        return self.EMPTY_ERROR_TEXT

    @property
    def data(self):
        return self._data

    @property
    def status_code(self):
        return self._status_code

    def done(self):
        if self._future.done():
            self._expose()
            return True
        return False

    def _expose(self):
        try:
            response = self._future.result()
            self._data = response.json()
            self._status_code = response.status_code
        except requests.exceptions.ConnectionError:
            raise APIError('Connection error')
        except requests.exceptions.InvalidURL:
            raise APIError('Invalid URL')
        except ValueError:
            raise APIError('Invalid JSON')


__all__ = [
    APIError,
    APIClient,
    APIResponse
]
