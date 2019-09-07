
import yaml

import lib.models


class InvalidServerStorage(Exception):
    def __init__(self, path):
        super().__init__('Invalid server storage: {}'.format(path))


class ServerRepository:
    def __init__(self, path):
        self.__path = path
        self.__servers = []

    def load(self):
        with open(self.__path) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if data is None:
                data = []

            if not isinstance(data, list):
                raise InvalidServerStorage(self.__path)

            self.__servers = list(lib.models.Server.from_yaml_dict(s) for s in data)

    reload = load

    def save(self):
        with open(self.__path, 'w') as f:
            yaml.dump(list(s.to_yaml_dict() for s in self.__servers), f)

    def get_list(self):
        return self.__servers

    def create(self, server: lib.models.Server):
        self.__servers.append(server)

    def delete(self, server: lib.models.Server):
        i = self.__servers.index(server)
        del self.__servers[i]
