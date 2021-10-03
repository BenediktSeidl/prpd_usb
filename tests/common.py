from prpd_usb.prpd import _PrPd
from prpd_usb.faker import DATA


class SerialFaker:
    def __init__(self, model=None):
        self._model = model
        self._next_answer = None

    def write(self, data):
        answers = DATA[data]
        if self._model in answers:
            self._next_answer = answers[self._model]
            return
        if None not in answers:
            raise Exception(f"can not use default model for {data.hex()}")
        self._next_answer = answers[None]

    def read(self, _length):
        if self._next_answer is None:
            raise Exception("have ot answer yet")
        else:
            result = self._next_answer
            self._next_answer = None
            return result

