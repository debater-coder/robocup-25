"""Gathers non-blocking input from USB serial to use as velocity commands."""
from sys import stdin
from select import poll, POLLIN


class CommandInput:
    """Polls stdin and builds a line of ASCII input, parsing as 3 floats."""
    def __init__(self):
        self._poll = poll()
        self._poll.register(stdin, POLLIN)
        self.line = ""

    def parse(self):
        result = tuple(map(float, self.line.split()))
        self.line = ""
        return result

    def poll(self):
        events = self._poll.poll(0)
        if events:
            char = stdin.read(1)

            if char == "\n":
                return self.parse()

            self.line += char

        return None
