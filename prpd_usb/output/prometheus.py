import re
import cherrypy

from .. import prpd


def format_labels(labels):
    return ",".join(f'{k}:"{v}"' for k, v in labels.items())


class Metrics:
    def __init__(self, reader):
        self._reader = reader

    @cherrypy.expose
    def metrics(self):
        result = []
        for command, field, time, value in self._reader.read():
            milliseconds_since_epoch = time * 1000
            prom_id = f"{command.name}_{field.name}"
            labels = {
                "unit": field.unit,
                "source": "prpd_usb",
            }
            phase = re.match(r".*(phase_\d)$", field.name)
            if phase:
                labels["phase"] = phase.groups()[0]

            result.append(
                f'#TYPE {prom_id} gauge\n'
                f'{prom_id}{{{format_labels(labels)}}} '
                f'{value} {milliseconds_since_epoch}\n',
            )
        cherrypy.response.headers['Content-Type'] = 'text/plain; version=0.0.4'
        return "".join(result)


def main(args):
    config = {'global': {
        'server.socket_host': args.bind,
        'server.socket_port': args.port,
        'engine.autoreload.on': False,
        'log.screen': False,
        'log.access_file': '',
        'log.error_file': '',
    }}
    with prpd.open(args) as reader:
        cherrypy.quickstart(Metrics(reader), '/', config)
