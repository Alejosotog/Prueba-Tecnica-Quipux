import time


class TTLCache:
    def __init__(self, ttl_seconds: int):
        self.ttl_seconds = ttl_seconds
        self._value = None
        self._expires_at = 0.0

    def get(self):
        if self._value is not None and time.monotonic() < self._expires_at:
            return self._value

        return None

    def set(self, value):
        self._value = value
        self._expires_at = time.monotonic() + self.ttl_seconds
