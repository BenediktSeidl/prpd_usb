import json

from .. import prpd


def main(args):
    with prpd.open(args) as reader:
        result = {}
        for command, field, _time, value in reader.read():
            group = result.setdefault(command.name, {})
            group[field.name] = value
        print(json.dumps(result, indent=4))
