

class GameObject:
    pass


class Updateable(GameObject):

    def update(self, dots: list):
        raise NotImplementedError


class Apple(GameObject):

    def __init__(self, id_: int, dot: tuple):
        self._id = id_
        self._dot = dot


class Snake(Updateable):

    def __init__(self, id_: int, dots: list):
        self._id = id_
        self._dots = dots

    def update(self, dots: list):
        pass


class Corpse(Updateable):

    def __init__(self, id_: int, dots: list):
        self._id = id_
        self._dots = dots

    def update(self, dots: list):
        pass


class Watermelon(Updateable):

    def __init__(self, id_: int, dots: list):
        self._id = id_
        self._dots = dots

    def update(self, dots: list):
        pass


class Wall(Updateable):

    def __init__(self, id_: int, dots: list):
        self._id = id_
        self._dots = dots

    def update(self, dots: list):
        pass
