from typing import overload


class Card:
    def __init__(self, value: int):
        self.id : str | None = None
        self._value = value
        self._visible = False

    def flip(self):
        self._visible = not self._visible

    def get_value(self, noneValue: int = None) -> int:
        return self._value if self._visible else noneValue

    def is_visible(self):
        return self._visible

    def peak(self):
        return self._value

    def __str__(self):
        return "{:<2}".format(str(self._value) if self._visible else "?")

    def __repr__(self):
        return "{:<2}".format(str(self._value) if self._visible else "?")
