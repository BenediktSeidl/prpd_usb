import json
import time

from paho.mqtt import publish

from .. import prpd


def main(prpd_reader, args):
    auth = {}
    if args.password and args.username:
        auth["password"] = args.password
        auth["username"] = args.username
    while True:
        messages = []
        for command, field, _time, value in prpd_reader.read():
            if args.payload_simple:
                payload = value
            else:
                payload = {
                    "value": value,
                    "unit": field.unit,
                }
            messages.append({
                "topic": f"{args.prefix}/{command.name}/{field.name}",
                "payload": json.dumps(payload),
            })
        publish.multiple(messages, hostname=args.hostname, port=args.port, auth=auth)
        time.sleep(args.interval)
