import json

from .. import prpd


def main(prpd_reader, args):
    result = {}
    for command, field, _time, value in prpd_reader.read():
        group = result.setdefault(command.name, {})
        group[field.name] = value
    print(json.dumps(result, indent=4))
