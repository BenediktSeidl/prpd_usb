import argparse
import logging

from . import __version__
from .faker import main as run_faker, DEVICES
from .output.stdout import main as run_stdout
from .output.prometheus import main as run_prometheus
from .output.mqtt import main as run_mqtt
from .output.mqtt_openwb import main as run_mqtt_openwb

def print_version(_):
    print(__version__)

def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(loglevel=[30])
    parser.add_argument(
        '-v', help='more verbose',
        dest='loglevel', const=-10, action='append_const')
    parser.add_argument(
        '-q', help='more quiet',
        dest='loglevel', const=+10, action='append_const')
    parser.add_argument(
        "--version", action='store_const', dest="func", const=print_version)

    parser.set_defaults(func=lambda options: parser.print_help())

    parser.add_argument(
        '--device', default="/dev/ttyUSB0")
    subparsers = parser.add_subparsers()
    parser.add_argument(
        '--model', help='Powerrouter Model (leave blank for auto detect)',
        choices=DEVICES,
    )

    p_faker = subparsers.add_parser(
        'faker', help='run helper that produces data like power router does')
    p_faker.add_argument(
        'serial_device', help='device or port to send fake data to',
    )
    p_faker.add_argument(
        'model', help='Powerrouter Model to fake',
        choices=DEVICES,
    )
    p_faker.set_defaults(func=run_faker)

    p_stdout = subparsers.add_parser(
        'stdout', help='read all data and output as json on stdout')
    p_stdout.set_defaults(func=run_stdout)

    p_prometheus = subparsers.add_parser(
        'prometheus', help='start a prometheus/open metrics endpoint')
    p_prometheus.add_argument("--bind", default="0.0.0.0")
    p_prometheus.add_argument("--port", default=9091, type=int)
    p_prometheus.set_defaults(func=run_prometheus)

    p_mqtt = subparsers.add_parser(
        'mqtt', help='publish data to mqtt')
    add_mqtt_args(p_mqtt)
    p_mqtt.add_argument("--prefix", default="prpd_usb")
    p_mqtt.add_argument("--payload-simple", action="store_true")
    p_mqtt.set_defaults(func=run_mqtt)

    p_mqtt_openwb = subparsers.add_parser(
        'mqtt-openwb', help='publish data to mqtt undestood by openwb')
    add_mqtt_args(p_mqtt_openwb)
    p_mqtt_openwb.set_defaults(func=run_mqtt_openwb)

    options = parser.parse_args()

    logging.basicConfig(
        level=max(10, min(50, sum(options.loglevel))),
        format="%(asctime)s %(levelname)s :: %(name)s :: %(message)s",
    )
    logging.warning("starting prpd_usb version %s", __version__)

    options.func(options)

def add_mqtt_args(subparser):
    subparser.add_argument("--hostname", default="localhost")
    subparser.add_argument("--port", default=1883, type=int)
    subparser.add_argument("--password")
    subparser.add_argument("--username")
    subparser.add_argument("--interval", default=30, type=int)
