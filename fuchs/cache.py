import typing

class Cache:
    """Class to cache the values defined during render"""
    __data: dict = dict()

    def store(self, key: str, value: typing.Any) -> None:
        """Registers a new value in the cache."""
        self.__data[key] = value


    @property
    def data(self) -> dict:
        return self.__data

class Counter(Cache):
    """Class to count"""
    __data: dict = dict(count=0)

    def incr(self) -> None:
        self.__data["count"] += 1

    def decr(self) -> None:
        self.__data["count"] -= 1

    def reset(self) -> None:
        self.__data["count"] = 0


    @property
    def data(self) -> dict:
        return self.__data