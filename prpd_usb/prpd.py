import logging
import time
from contextlib import contextmanager
import struct

import serial
import libscrc

from .schema import SCHEMA, FieldResult

logger = logging.getLogger(__name__)


@contextmanager
def open(args):
    logger.info("opening serial port '%s'", args.device)
    with serial.Serial(args.device, 115200, timeout=2) as ser:
        logger.debug("successfully opened serial port '%s'", args.device)
        yield PrPd(ser)


def crc(data):
    return bytes(struct.pack('>H', libscrc.modbus(data)))


class PrPd:
    def __init__(self, serial):
        self._serial = serial

    def read(self):
        for command in SCHEMA:
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
            time_response = time.time()
            logger.debug("got response with %i bytes", response_length)

            if response_length != expected_response_length:
                raise Exception(f"could not read {expected_response_length} bytes")
            if crc(response[:-3]) != response[-3:-1]:
                raise Exception("crc does not match")

            unpacked = struct.unpack(response_format, response[6:-3])
            for field, response in zip(command.fields, unpacked):
                if field.name is None:
                    continue
                yield FieldResult(command, field, time_response, response * field.factor)
