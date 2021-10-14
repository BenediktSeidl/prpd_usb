import logging
import time
from contextlib import contextmanager
import struct
import threading

import serial
import libscrc

from .schema import commands_by_model, FieldResult, CMD_MODEL, MODELS

logger = logging.getLogger(__name__)


@contextmanager
def open(args):
    if not args.open_prpd:
        yield None
        return
    logger.info("opening serial port '%s'", args.device)
    with serial.Serial(args.device, 115200, timeout=2) as ser:
        logger.debug("successfully opened serial port '%s'", args.device)
        prpd = _PrPd(ser)
        prpd.init(args.model)
        yield prpd


def crc(data):
    return bytes(struct.pack('>H', libscrc.modbus(data)))


class _PrPd:
    def __init__(self, serial):
        self.lock = threading.Lock()  # run two outputs in parallel
        self._serial = serial
        self._model = None

    def _command(self, command):
        request = bytes.fromhex(command.command)
        response_format = ">" + "".join(f.type for f in command.fields)
        expected_response_length = struct.calcsize(response_format) + 9
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(
                f"sent request {request.hex()}, "
                f"waiting for {expected_response_length} bytes response")
        self._serial.write(request)
        response = self._serial.read(expected_response_length)
        response_length = len(response)
        logger.debug("got response with %i bytes", response_length)

        if response_length != expected_response_length:
            raise Exception(f"could not read {expected_response_length} bytes")
        crc_expected = crc(response[:-3])
        crc_actual = response[-3:-1]
        if crc_expected != crc_actual:
            raise Exception(f"crc does not match, got {crc_actual.hex()}, expected {crc_expected.hex()}")
        unpacked = struct.unpack(response_format, response[6:-3])
        return unpacked

    def _get_commands(self):
        return commands_by_model(self._model)

    def init(self, model=None):
        if model is not None:
            self._model = model
            return
        model, serial_number = self._command(CMD_MODEL)
        model = model.decode('ascii')
        logger.info("Found model %s with serialnumber %s", model, serial_number)
        if model not in MODELS:
            raise Exception(
                f"Model '{model}' is not know yet. You can try "
                "to specify another model via --model, or open an issue")
        self._model = MODELS[model]
        logger.info(f"Identified model {self._model}")

    @property
    def model(self):
        return self._model

    def read(self):
        with self.lock:
            for command in self._get_commands():
                time_response = time.time()
                unpacked = self._command(command)
                for field, response in zip(command.fields, unpacked):
                    if field.name is None:
                        continue
                    yield FieldResult(command, field, time_response, response * field.factor)
