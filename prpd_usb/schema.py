from collections import namedtuple

Command = namedtuple("Command", ["name", "command", "fields"])
Field = namedtuple("Field", ["type", "name", "unit", "factor"])

FieldResult = namedtuple("FieldResult", ["command", "field", "time", "value"])

MODEL_TO_COMMANDS = {
        "PR37Bi": ["7105", "7104", "7103", "7005", "7001", "7101", "7004", "7003"],
        "PR37SB": ["7001", "7002", "7003", "7004", "7101", "7102", "7103", "7104"],
        "PR50SB": ["7104", "7103", "7001", "7101", "7004", "7003", "7002", "7102"],
}

_COMMANDS = [
    Command("solar", "5a0071050000dc07a5", [
        Field('I', "total_phase_1", "Wh", 1),
        Field('I', "total_phase_2", "Wh", 1),
        Field('I', "total_phase_3", "Wh", 1),
    ]),
    Command("grid", "5a00710400001c56a5", [
        Field('I', "total_phase_1", "Wh", 1),
        Field('I', "total_phase_2", "Wh", 1),
        Field('I', "total_phase_3", "Wh", 1),
    ]),
    Command("platform", "5a0071030000dde7a5", [
        Field('I', 'consumed', "Wh", 1),
        Field('I', 'produced', "Wh", 1),
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
        Field('H', 'voltage', "V", 0.01),
        Field('i', 'current', "A", 0.01),
        Field('H', None, None, None),
        Field('I', None, None, None),
        Field('h', 'power', "W", 1),
        Field('B', 'soc', "%", 1),
        Field('h', 'temp1', "°C", 0.1),
        Field('h', 'temp2', "°C", 0.1),
        Field('H', None, None, None),
    ]),
    Command("battery", "5a00710100001d46a5", [
        Field('I', 'consumed', "Wh", 1),
        Field('I', 'produced', "Wh", 1),
    ]),
    Command("grid", "5a0070040000e057a5", [
        Field('H', None, None, None),
        Field('h', 'current_phase_1', "A", 0.01),
        Field('h', 'current_phase_2', "A", 0.01),
        Field('h', 'current_phase_3', "A", 0.01),

        Field('H', 'voltage_phase_1', "V", 0.1),
        Field('H', 'voltage_phase_2', "V", 0.1),
        Field('H', 'voltage_phase_3', "V", 0.1),

        Field('h', 'power_w_phase_1', "W", 1),
        Field('h', 'power_w_phase_2', "W", 1),
        Field('h', 'power_w_phase_3', "W", 1),

        Field('H', 'power_va_phase_1', "VA", 1),
        Field('H', 'power_va_phase_2', "VA", 1),
        Field('H', 'power_va_phase_3', "VA", 1),
    ]),
    Command("platform", "5a007003000021e6a5", [
        Field('H', 'frequency', "Hz", 0.01),
        Field('H', 'voltage', "V", 0.1),
        Field('h', 'temp', "°C", 0.1),
        Field('H', 'status', "", 1),
        Field('h', 'power', "W", 1),
    ]),
    Command("solar", "5a0070020000e1b7a5", [
        Field('H', 'voltage_string_1', "V", 0.01),
        Field('i', 'current_string_1', "A", 0.01),
        Field('H', 'voltage_string_2', "V", 0.01),
        Field('i', 'current_string_2', "A", 0.01),
        Field('H', 'status', "", 1),
        Field('H', None, None, None),
        Field('H', None, None, None),
        Field('H', None, None, None),
        Field('H', None, None, None),
    ]),
    Command("solar", "5a00710200001db6a5", [
        Field('I', "total_string_1", "Wh", 1),
        Field('I', "total_string_2", "Wh", 1),
        Field('I', "total", "Wh", 1),
    ]),
]

COMMANDS = {c.command[4:8]: c for c in _COMMANDS}

CMD_MODEL = Command("platform", "5a0052500000481ca5", [
    Field('7s', 'model', None, None),
    Field('9s', 'serialnumber', None, None),
])

MODELS = {
    "9563369": "PR50SB",
    "9564225": "PR37Bi",
    "9561773": "PR37SB",
}

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


def commands_by_model(model):
    for command in MODEL_TO_COMMANDS[model]:
        yield COMMANDS[command]
