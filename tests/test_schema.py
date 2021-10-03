from prpd_usb.prpd import _PrPd
from prpd_usb.faker import DATA
from prpd_usb.output.stdout import to_json


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


def test_pr37bi():
    prpd = _PrPd(SerialFaker("PR37Bi"))
    prpd.init()
    result = to_json((prpd.read()))
    assert result == {
        "battery": {
            "consumed": 5868399,
            "current": 6.18,
            "power": 332,
            "produced": 5545710,
            "soc": 76,
            "temp1": 22.0,
            "temp2": 47.1,
            "voltage": 54.51,
        },
        "grid": {
            "current_phase_1": 11.700000000000001,
            "current_phase_2": 9.700000000000001,
            "current_phase_3": 3.2,
            "power_va_phase_1": 263,
            "power_va_phase_2": 214,
            "power_va_phase_3": 73,
            "power_w_phase_1": -242,
            "power_w_phase_2": 213,
            "power_w_phase_3": 47,
            "total_phase_1": 7872100,
            "total_phase_2": 4909000,
            "total_phase_3": 4309400,
            "voltage_phase_1": 225.0,
            "voltage_phase_2": 225.60000000000002,
            "voltage_phase_3": 223.60000000000002,
        },
        "platform": {
            "consumed": 5028182,
            "frequency": 49.99,
            "power": 18,
            "produced": 13789973,
            "status": 51475,
            "temp": 20.0,
            "voltage": 223.9,
        },
        "solar": {
            "status": 1043,
            "total_phase_1": 0,
            "total_phase_2": 0,
            "total_phase_3": 25054400,
            "va_phase_1": 0,
            "va_phase_2": 9,
            "va_phase_3": 14,
            "w_phase_1": 0,
            "w_phase_2": -3,
            "w_phase_3": -1,
        },
    }


def test_pr50sb():
    prpd = _PrPd(SerialFaker("PR50SB"))
    prpd.init()
    result = to_json((prpd.read()))
    assert result == {
        "battery": {
            "consumed": 5868399,
            "current": 6.18,
            "power": 332,
            "produced": 5545710,
            "soc": 76,
            "temp1": 22.0,
            "temp2": 47.1,
            "voltage": 54.51,
        },
        "grid": {
            "current_phase_1": 11.700000000000001,
            "current_phase_2": 9.700000000000001,
            "current_phase_3": 3.2,
            "power_va_phase_1": 263,
            "power_va_phase_2": 214,
            "power_va_phase_3": 73,
            "power_w_phase_1": -242,
            "power_w_phase_2": 213,
            "power_w_phase_3": 47,
            "total_phase_1": 7872100,
            "total_phase_2": 4909000,
            "total_phase_3": 4309400,
            "voltage_phase_1": 225.0,
            "voltage_phase_2": 225.60000000000002,
            "voltage_phase_3": 223.60000000000002,
        },
        "platform": {
            "consumed": 5028182,
            "frequency": 49.99,
            "power": 18,
            "produced": 13789973,
            "status": 51475,
            "temp": 20.0,
            "voltage": 223.9,
        },
        "solar": {
            "current_string_1": 4.25,
            "current_string_2": 4.26,
            "status": 61507,
            "total": 21155632,
            "total_string_1": 10610074,
            "total_string_2": 10545559,
            "voltage_string_1": 291.40000000000003,
            "voltage_string_2": 291.1,
        },
    }
