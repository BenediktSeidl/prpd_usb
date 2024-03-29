from prpd_usb.prpd import _PrPd
from prpd_usb.output.stdout import to_json

from .common import SerialFaker

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
            "current_phase_1": 1.17,
            "current_phase_2": 0.97,
            "current_phase_3": 0.32,
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


def test_pr37sb():
    prpd = _PrPd(SerialFaker("PR37SB"))
    prpd.init()
    result = to_json((prpd.read()))
    assert result == {
        "battery": {
            "consumed": 5806854,
            "current": -19.02,
            "power": -502,
            "produced": 4497664,
            "soc": 78,
            "temp1": 26.8,
            "temp2": 46.1,
            "voltage": 26.0,
        },
        "grid": {
            "current_phase_1": 1.06,
            "current_phase_2": 2.90,
            "current_phase_3": 3.79,
            "power_va_phase_1": 241,
            "power_va_phase_2": 653,
            "power_va_phase_3": 867,
            "power_w_phase_1": 209,
            "power_w_phase_2": 622,
            "power_w_phase_3": -847,
            "total_phase_1": 7872100,
            "total_phase_2": 4909000,
            "total_phase_3": 4309400,
            "voltage_phase_1": 227.20000000000002,
            "voltage_phase_2": 227.0,
            "voltage_phase_3": 227.4,
        },
        "platform": {
            "consumed": 57868920,
            "frequency": 50.01,
            "power": 4,
            "produced": 1657152,
            "status": 18707,
            "temp": 31.0,
            "voltage": 229.0,
        },
        "solar": {
            "current_string_1": 5.78,
            "current_string_2": 5.86,
            "status": 61507,
            "total": 20722671,
            "total_string_1": 10168204,
            "total_string_2": 10554467,
            "voltage_string_1": 189.09,
            "voltage_string_2": 185.01,
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
            "current_phase_1": 1.17,
            "current_phase_2": 0.97,
            "current_phase_3": 0.32,
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
