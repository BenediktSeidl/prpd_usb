from functools import partial
import threading

from cherrypy import engine

from .mqtt_openwb import main as run_mqtt_openwb
from .prometheus import main as run_prometheus


def main(prpd_reader, options):
    prom_thread = threading.Thread(
        target=partial(run_prometheus, prpd_reader, options),
        name="prpd_output_prom",
    )
    prom_thread.start()
    try:
        run_mqtt_openwb(prpd_reader, options)
    except KeyboardInterrupt:
        pass
    engine.exit()
