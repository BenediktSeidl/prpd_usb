import json

from .. import prpd

def to_json(prpd_result):
    result = {}
    for command, field, _time, value in prpd_result:
        group = result.setdefault(command.name, {})
        group[field.name] = value
    return result


def main(prpd_reader, args):
    result = to_json(prpd_reader.read())
    print(json.dumps(result, indent=4))
