__all__ = (
    "SplitType",
    "A2SPacketType",
)

from enum import IntEnum


class SplitType(IntEnum):
    NOT_SPLIT = -1
    SPLIT = -2

    UNKNOWN = 69420

    @classmethod
    def _missing_(cls, _: int) -> "SplitType":
        return SplitType.UNKNOWN


class A2SPacketType(IntEnum):
    A2S_INFO = 0x54  # 'T'
    A2S_PLAYER = 0x55  # 'U'
    S2C_CHALLENGE = 0x41  # 'A'

    A2S_INFO_RESPONSE = 0x49  # 'I'
    A2S_PLAYER_RESPONSE = 0x44  # 'D'

    UNKNOWN = 69420  # xd hehe lel

    @classmethod
    def _missing_(cls, _: int) -> "A2SPacketType":
        return A2SPacketType.UNKNOWN
