import json
import time
from collections import namedtuple

from paho.mqtt import publish


Direct = namedtuple('Direct', ['key'])
Map = namedtuple('Map', ['keys', 'function'])
MultiMap = namedtuple('Map', ['keys', 'functions'])

def _neg(value):
    return value * -1

def _sum(*values):
    return sum(values)

def _m_sum(*values):
    return [sum(values)]

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

    "openWB/set/pv/1/W": MultiMap(keys=(('solar', 'w_phase_1'), ('solar', 'w_phase_2'), ('solar', 'w_phase_3'),), functions=(_m_sum, _neg)),
    "openWB/set/pv/1/WhCounter": Map(keys=(('solar', 'total_phase_1'), ('solar', 'total_phase_2'), ('solar', 'total_phase_3')), function=_sum),

    "openWB/set/houseBattery/W": Map(keys=(('battery', 'power'),), function=_neg),
    "openWB/set/houseBattery/WhImported": Direct(('battery', 'consumed')),
    "openWB/set/houseBattery/WhExported": Direct(('battery', 'produced')),
    "openWB/set/houseBattery/%Soc": Direct(('battery', 'soc')),
}


def transform_to_openwb(prpd_data):
    messages = []
    data = {}

    for command, field, _time, value in prpd_data:
        data[(command.name, field.name)] = value

    for topic, mapping in MAPPING.items():
        if isinstance(mapping, Direct):
            payload = data[mapping.key]
        elif isinstance(mapping, MultiMap):
            values = [data[k] for k in mapping.keys]
            for function in mapping.functions:
                values = function(*values)
            payload = values
        else:
            keys = [data[k] for k in mapping.keys]
            payload = mapping.function(*keys)

        messages.append({
            "topic": topic,
            "payload": json.dumps(payload),
        })
    return messages


def main(prpd_reader, args):
    auth = {}
    if args.mqtt_password and args.mqtt_username:
        auth["password"] = args.mqtt_password
        auth["username"] = args.mqtt_username
    while True:

        data = prpd_reader.read()
        messages = transform_to_openwb(data)

        publish.multiple(messages, hostname=args.mqtt_hostname, port=args.mqtt_port, auth=auth)
        time.sleep(args.mqtt_interval)
