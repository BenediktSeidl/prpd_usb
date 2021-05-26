import json
import time
from collections import namedtuple

from paho.mqtt import publish

from .. import prpd

Direct = namedtuple('Direct', ['key'])
Map = namedtuple('Map', ['keys', 'function'])

def _neg(value):
    return value * -1

def _sum(*values):
    return sum(values)

MAPPING = {
    "openWB/set/evu/W": Map(keys=(('grid', 'power_w_phase_1'), ('grid', 'power_w_phase_2'), ('grid', 'power_w_phase_3')), function=_sum),
    "openWB/set/evu/APhase1": Direct(('grid', 'current_phase_1')),
    "openWB/set/evu/APhase2": Direct(('grid', 'current_phase_2')),
    "openWB/set/evu/APhase3": Direct(('grid', 'current_phase_3')),
    "openWB/set/evu/WhImported": Map(keys=(('grid', 'total_phase_1'), ('grid', 'total_phase_2'), ('grid', 'total_phase_3')), function=_sum),
    "openWB/set/evu/WhExported": Map(keys=(('solar', 'total_phase_1'), ('solar', 'total_phase_2'), ('solar', 'total_phase_3')), function=_sum),
    "openWB/set/evu/VPhase1": Direct(('grid', 'voltage_phase_1')),
    "openWB/set/evu/VPhase2": Direct(('grid', 'voltage_phase_2')),
    "openWB/set/evu/VPhase3": Direct(('grid', 'voltage_phase_3')),
    "openWB/set/evu/HzFrequenz": Direct(('platform', 'frequency')),

    "openWB/set/pv/1/W": Map(keys=(('solar', 'w_phase_3'),), function=_neg),
    "openWB/set/pv/1/WhCounter": Direct(('solar', 'total_phase_3')),

    "openWB/set/houseBattery/W": Map(keys=(('battery', 'power'),), function=_neg),
    "openWB/set/houseBattery/WhImported": Direct(('battery', 'consumed')),
    "openWB/set/houseBattery/WhExported": Direct(('battery', 'produced')),
    "openWB/set/houseBattery/%Soc": Direct(('battery', 'soc')),
}


def main(args):
    auth = {}
    if args.password and args.username:
        auth["password"] = args.password
        auth["username"] = args.username
    while True:
        messages = []
        data = {}

        with prpd.open(args) as reader:
            for command, field, _time, value in reader.read():
                data[(command.name, field.name)] = value

        for topic, mapping in MAPPING.items():
            if isinstance(mapping, Direct):
                payload = data[mapping.key]
            else:
                keys = [data[k] for k in mapping.keys]
                payload = mapping.function(*keys)

            messages.append({
                "topic": topic,
                "payload": json.dumps(payload),
            })

        publish.multiple(messages, hostname=args.hostname, port=args.port, auth=auth)
        time.sleep(args.interval)
