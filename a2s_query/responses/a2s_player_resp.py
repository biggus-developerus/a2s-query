__all__ = ("A2SPlayerResp",)

from dataclasses import dataclass, field
from io import BytesIO
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from a2s_query.packet import A2SPacket

from a2s_query.utils import get_float, get_int, get_str


class PlayerInfo(TypedDict):
    index: int
    name: str
    score: int
    duration: float


@dataclass
class A2SPlayerResp:
    @staticmethod
    def from_packet(packet: "A2SPacket") -> "A2SPlayerResp":
        info = A2SPlayerResp()

        data = BytesIO(packet.payload)
        info.player_info_count = get_int(1, data)

        for _ in range(info.player_info_count):
            info.players.append(
                {
                    "index": get_int(1, data),
                    "name": get_str(data),
                    "score": get_int(2, data),
                    "duration": get_float(4, data),
                }
            )

        return info

    player_info_count: int = 0
    players: list[PlayerInfo] = field(default_factory=list)
