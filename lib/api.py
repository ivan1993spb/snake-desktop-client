from requests.sessions import Session
from requests.utils import CaseInsensitiveDict
import requests.exceptions
import requests


class APIError(Exception):
    pass


class APIResponseError(APIError):
    def __init__(self, status, text):
        super().__init__('Response error: status={}, text={}'.format(status, text))


class APIClient(Session):

    __USER_AGENT_DEFAULT = 'SnakeAPIClient'

    def __init__(self, entrypoint: str, user_agent=None):
        assert entrypoint.endswith('api'), 'API entrypoint has to end with suffix "api"'

        super().__init__()
        self._entrypoint = entrypoint
        self._user_agent = user_agent if user_agent else self.__USER_AGENT_DEFAULT

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
        return '/'.join((self._entrypoint,)+argv)

    def _call(self, method: str, url: str, data=None):
        try:
            response = self.request(method.upper(), url, data=data)
            response_data = response.json()

            if response.status_code in [200, 201]:
                return response_data

            assert isinstance(response_data, dict)

            raise APIResponseError(response.status_code, response_data.get('text', 'empty text'))
        except requests.exceptions.ConnectionError:
            raise APIError('Connection error')
        except ValueError:
            raise APIError('Invalid json in API response')
