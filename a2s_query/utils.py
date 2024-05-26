__all__ = (
    "get_int",
    "get_str",
)

import struct
from io import BytesIO


def get_str(data: BytesIO) -> str:
    result_str = b""
    i = 0

    while i < data.getbuffer().nbytes:
        c = data.read(1)

        if c == b"\x00":
            break
        result_str += c

    return result_str.decode("utf-8")


def get_int(size: int, data: BytesIO) -> int:
    val = data.read(size)
    return int.from_bytes(val, "little")


def get_float(size: int, data: BytesIO) -> float:
    val = data.read(size)

    if size == 4:
        return struct.unpack("<f", val)[0]
    elif size == 8:
        return struct.unpack("<d", val)[0]
