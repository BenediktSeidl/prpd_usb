import logging

import serial

logger = logging.getLogger(__name__)


DATA = dict([
    (
        bytes.fromhex("5a0071050000dc07a5"),
        bytes.fromhex("5aff7105000c0000000000000000017e4cc02057a5"),
    ), (
        bytes.fromhex("5a00710400001c56a5"),
        bytes.fromhex("5aff7104000c00781e64004ae7c80041c198baa4a5"),
    ), (
        bytes.fromhex("5a0071030000dde7a5"),
        bytes.fromhex("5aff71030008004cb95600d26b153ae0a5"),
    ), (
        bytes.fromhex("5a00700500002006a5"),
        bytes.fromhex("5aff7005000e04130000fffdffff00000009000e5f95a5"),
    ), (
        bytes.fromhex("5a0070010000e147a5"),
        bytes.fromhex("5aff70010015154b0000026a0000031b4143014c4c00dc01d700005df6a5"),
    ), (
        bytes.fromhex("5a00710100001d46a5"),
        bytes.fromhex("5aff7101000800598b6f00549eee6ed0a5"),
    ), (
        bytes.fromhex("5a0070040000e057a5"),
        bytes.fromhex("5aff7004001a051300750061002008ca08d008bcff0e00d5002f010700d600492725a5"),
    ), (
        bytes.fromhex("5a0031040000dc43a5"),
        bytes.fromhex("5aff31040006000da0045c9b9cbca5"),
    ), (
        bytes.fromhex("5a00230000006507a5"),
        bytes.fromhex("5aff230000170218bfcb991e3b6c0c0b0a0d0c0b0a000000000d0c0b0ae019a5"),
    ), (
        bytes.fromhex("5a007003000021e6a5"),
        bytes.fromhex("5aff7003000a138708bf00c8c913001205b8a5"),
    )
])

def main(args):
    with serial.Serial(args.serial_device, 115200) as ser:
        logger.info("opened serial port %s", args.serial_device)
        read_buffer = bytes([0]*9)
        while True:
            byte = ser.read()
            read_buffer = read_buffer[1:] + byte
            logger.debug("current read_buffer %s", read_buffer.hex())
            if read_buffer in DATA:
                logging.info("found command, sending response")
                ser.write(DATA[read_buffer])
