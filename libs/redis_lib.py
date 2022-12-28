from redis import Redis


class RedisLib:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._connection = None

    def connect(self):
        self._connection: Redis = Redis(host=self._host, port=self._port)

    def set(self, key, value):
        if self._connection is not None:
            self._connection.set(key, value)

    def get(self, key):
        if self._connection is not None:
            return self._connection.get(key).decode()

    def disconnect(self):
        self._connection = None
