class Card:
    def __init__(self, value: int):
        self._value = value
        self._visible = False

    def flip(self):
        self._visible = not self._visible

    def get_value(self):
        return self._value if self._visible else None
    