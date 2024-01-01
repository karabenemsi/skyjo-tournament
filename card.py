class Card:
    def __init__(self, value: int):
        self._value = value
        self._visible = False

    def flip(self):
        self._visible = not self._visible

    def get_value(self):
        return self._value if self._visible else None

    def peak(self):
        return self._value

    def __str__(self):
        return "{:<2}".format(str(self._value) if self._visible else "?")

    def __repr__(self):
        return "{:<2}".format(str(self._value) if self._visible else "?")
