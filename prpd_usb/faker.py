import logging
from itertools import chain

import serial

logger = logging.getLogger(__name__)

h = bytes.fromhex

DATA = dict([
    (
        h("5a0052500000481ca5"), {
            "PR37Bi": h("5aff52500010393536343232355858585858585858583d97a5"),
            "PR50SB": h("5aff5250001039353633333639585858585858585858b6b4a5"),
            "PR37SB": h("5aff5250001039353631373733483432364238373136b1b7a5"),
            "UNKNOWN": h("5aff5250001039393939393939585858585858585858ba87a5")}
    ), (
        h("5a0070020000e1b7a5"), {
            "PR37SB": h("5aff7002001649dd0000024248450000024af0430882021c0226052404b3a5"),
            "PR50SB": h("5aff7002001671d4000001a971b6000001aaf04309b0020801d60522150ea5")}

    ), (
        h("5a00710200001db6a5"), {
            "PR37SB": h("5aff7102000c009b278c00a10c63013c33ef84f9a5"),
            "PR50SB": h("5aff7102000c00a1e59a00a0e9970142cf306ab2a5")}
    ), (
        h("5a0071050000dc07a5"), {
            "PR37SB": h("5aff7105000c0000000000000000000000005402a5"),
            "PR37Bi": h("5aff7105000c0000000000000000017e4cc02057a5"),
            "PR50SB": h("5aff7105000c0000000000000000000000005402a5")},
    ), (
        h("5a00710400001c56a5"), {
            None: h("5aff7104000c00781e64004ae7c80041c198baa4a5")},
    ), (
        h("5a0071030000dde7a5"), {
            "PR37SB": h("5aff7103000803730278001949400035a5"),
            None: h("5aff71030008004cb95600d26b153ae0a5")},
    ), (
        h("5a00700500002006a5"), {
            "PR37SB": h("5aff7005000e0010000000000000000000000000f2eda5"),
            "PR37Bi": h("5aff7005000e04130000fffdffff00000009000e5f95a5"),
            # PR50SB: status 16 could mean not connected?!
            "PR50SB": h("5aff7005000e0010000000000000000000000000f2eda5")},
    ), (
        h("5a0070010000e147a5"), {
            "PR37SB": h("5aff700100150a28fffff892000006cc4b43fe0a4e010c01cd06c02dc9a5"),
            None: h("5aff70010015154b0000026a0000031b4143014c4c00dc01d700005df6a5")},
    ), (
        h("5a00710100001d46a5"), {
            "PR37SB": h("5aff7101000800589b060044a1004e0ea5"),
            None: h("5aff7101000800598b6f00549eee6ed0a5")},
    ), (
        h("5a0070040000e057a5"), {
            "PR37SB": h("5aff7004001a0713006a0122017b08e008de08e200d1026efcb100f1028d0363f2faa5"),
            None: h("5aff7004001a051300750061002008ca08d008bcff0e00d5002f010700d600492725a5")},
    ), (
        h("5a0031040000dc43a5"), {
            "PR37SB": h("5aff31040006000da0046199cd2da5"),
            None: h("5aff31040006000da0045c9b9cbca5")},
    ), (
        h("5a00230000006507a5"), {
            None: h("5aff230000170218bfcb991e3b6c0c0b0a0d0c0b0a000000000d0c0b0ae019a5")},
    ), (
        h("5a007003000021e6a5"), {
            "PR37SB": h("5aff7003000a138908f20136491300046ae9a5"),
            None: h("5aff7003000a138708bf00c8c913001205b8a5")},
    )
])
DEVICES = set(i for i in chain.from_iterable(v.keys()
              for v in DATA.values()) if i is not None)


def main(_, args):
    with serial.Serial(args.serial_device, 115200) as ser:
        logger.info("opened serial port %s", args.serial_device)
        read_buffer = bytes([0]*9)
        while True:
            byte = ser.read()
            read_buffer = read_buffer[1:] + byte
            logger.debug("current read_buffer %s", read_buffer.hex())
            if read_buffer in DATA:
                logging.info("found command, sending response")
                answer = DATA[read_buffer]
                if args.model in answer:
                    response = answer[args.model]
                elif None in answer:
                    response = answer[None]
                else:
                    logging.error("could not find answer for this model!")
                    continue
                ser.write(response)
            else:
                logging.error("command not found")
