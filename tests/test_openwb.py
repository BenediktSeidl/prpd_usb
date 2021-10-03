from prpd_usb.prpd import _PrPd
from prpd_usb.output.stdout import to_json
from prpd_usb.output.mqtt_openwb import transform_to_openwb

from .common import SerialFaker


def test_openwb_37bi():
    prpd = _PrPd(SerialFaker("PR37Bi"))
    prpd.init()
    data = prpd.read()
    messages = transform_to_openwb(data)
    assert messages == [
        {"payload": "18", "topic": "openWB/set/evu/W"},
        {"payload": "1.17", "topic": "openWB/set/evu/APhase1"},
        {"payload": "0.97", "topic": "openWB/set/evu/APhase2"},
        {"payload": "0.32", "topic": "openWB/set/evu/APhase3"},
        {"payload": "17090500", "topic": "openWB/set/evu/WhImported"},
        {"payload": "25054400", "topic": "openWB/set/evu/WhExported"},
        {"payload": "225.0", "topic": "openWB/set/evu/VPhase1"},
        {"payload": "225.60000000000002", "topic": "openWB/set/evu/VPhase2"},
        {"payload": "223.60000000000002", "topic": "openWB/set/evu/VPhase3"},
        {"payload": "49.99", "topic": "openWB/set/evu/HzFrequenz"},
        {"payload": "1", "topic": "openWB/set/pv/1/W"},
        {"payload": "25054400", "topic": "openWB/set/pv/1/WhCounter"},
        {"payload": "-332", "topic": "openWB/set/houseBattery/W"},
        {"payload": "5868399", "topic": "openWB/set/houseBattery/WhImported"},
        {"payload": "5545710", "topic": "openWB/set/houseBattery/WhExported"},
        {"payload": "76", "topic": "openWB/set/houseBattery/%Soc"},
    ]
