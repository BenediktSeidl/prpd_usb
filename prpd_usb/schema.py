from collections import namedtuple

Command = namedtuple("Command", ["name", "command", "fields"])
Field = namedtuple("Field", ["type", "name", "unit", "factor"])

FieldResult = namedtuple("FieldResult", ["command", "field", "time", "value"])

SCHEMA = [
    Command("solar", "5a0071050000dc07a5", [
        Field('I', "total_phase_1", "kWh", 1),
        Field('I', "total_phase_2", "kWh", 1),
        Field('I', "total_phase_3", "kWh", 1),
    ]),
    Command("grid", "5a00710400001c56a5", [
        Field('I', "total_phase_1", "kWh", 1),
        Field('I', "total_phase_2", "kWh", 1),
        Field('I', "total_phase_3", "kWh", 1),
    ]),
    Command("platform", "5a0071030000dde7a5", [
        Field('I', 'consumed', "kWh", 1),
        Field('I', 'produced', "kWh", 1),
    ]),
    Command("solar", "5a00700500002006a5", [
        Field('H', 'status', "", 1),
        Field('h', 'w_phase_1', "W", 1),
        Field('h', 'w_phase_2', "W", 1),
        Field('h', 'w_phase_3', "W", 1),
        Field('H', 'va_phase_1', "VA", 1),
        Field('H', 'va_phase_2', "VA", 1),
        Field('H', 'va_phase_3', "VA", 1),
    ]),
    Command("battery", "5a0070010000e147a5", [
        Field('H', 'voltage', "V", 1),
        Field('i', 'current', "A", 1),
        Field('H', None, None, None),
        Field('I', None, None, None),
        Field('h', 'power', "W", 1),
        Field('B', 'soc', "%", 1),
        Field('h', 'temp1', "°C", 0.1),
        Field('h', 'temp2', "°C", 0.1),
        Field('H', None, None, None),
    ]),
    Command("battery", "5a00710100001d46a5", [
        Field('I', 'consumed', "kWh", 1),
        Field('I', 'produced', "kWh", 1),
    ]),
    Command("grid", "5a0070040000e057a5", [
        Field('H', None, None, None),
        Field('h', 'current_phase_1', "A", 1),
        Field('h', 'current_phase_2', "A", 1),
        Field('h', 'current_phase_3', "A", 1),

        Field('H', 'voltage_phase_1', "V", 1),
        Field('H', 'voltage_phase_2', "V", 1),
        Field('H', 'voltage_phase_3', "V", 1),

        Field('h', 'power_w_phase_1', "W", 1),
        Field('h', 'power_w_phase_2', "W", 1),
        Field('h', 'power_w_phase_3', "W", 1),

        Field('H', 'power_va_phase_1', "VA", 1),
        Field('H', 'power_va_phase_2', "VA", 1),
        Field('H', 'power_va_phase_3', "VA", 1),
    ]),
    Command("platform", "5a007003000021e6a5", [
        Field('H', 'fequency', "Hz", 0.01),
        Field('H', 'voltage', "V", 0.1),
        Field('h', 'temp', "°C", 0.1),
        Field('H', 'status', "", 1),
        Field('h', 'power', "W", 1),
    ]),
]

NETWORK = [
    Command("mac_address", "5a0031040000dc43a5", [
        Field('bbbbbb', 'mac_address', None, None),
    ]),
    Command("network", "5a00230000006507a5", [
        Field('B', None, None, None),
        Field('I', None, None, None),
        Field('h', None, None, None),
        Field('I', 'ip_address', "", 1),
        Field('I', 'dns1', "", 1),
        Field('I', 'dns2', "", 1),
        Field('I', 'gateway', "", 1),
    ]),
]
