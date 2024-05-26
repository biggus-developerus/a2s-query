__all__ = ("A2SInfoResp",)

from dataclasses import dataclass
from io import BytesIO
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from a2s_query.packet import A2SPacket

from a2s_query.utils import get_int, get_str


@dataclass
class A2SInfoResp:
    @staticmethod
    def from_packet(packet: "A2SPacket") -> "A2SInfoResp":
        info = A2SInfoResp()

        data = BytesIO(packet.payload)

        info.protocol_version = get_int(1, data)
        info.server_name = get_str(data)
        info.map_name = get_str(data)
        info.folder_name = get_str(data)
        info.game_name = get_str(data)

        info.steam_app_id = get_int(2, data)
        info.player_count = get_int(1, data)
        info.max_players = get_int(1, data)
        info.bot_count = get_int(1, data)

        info.server_type = data.read(1).decode("utf-8")
        info.server_environment = data.read(1).decode("utf-8")
        info.server_visability = bool(data.read(1))
        info.server_vac = bool(data.read(1))

        info.game_version = get_str(data)

        info.extra_data_flag = int.from_bytes(data.read(1), "little")
        edf = info.extra_data_flag

        info.game_server_port = get_int(2, data) if edf & 0x80 else 0
        info.server_steam_id = get_int(8, data) if edf & 0x10 else 0

        if edf & 0x40:
            info.sourcetv_server_port = get_int(2, data)
            info.sourcetv_server_name = get_str(data)

        info.server_tags = get_str(data) if edf & 0x20 else ""
        info.game_id = get_int(8, data) if edf & 0x01 else 0

        return info

    protocol_version: Optional[int] = None

    server_name: str = ""
    map_name: str = ""
    folder_name: str = ""
    game_name: str = ""

    steam_app_id: int = 0

    player_count: int = 0
    max_players: int = 0
    bot_count: int = 0

    server_type: str = ""  # make enum
    server_environment: str = ""  # make enum
    server_visability: bool = False
    server_vac: bool = False

    game_version: str = ""

    extra_data_flag: int = 0

    game_server_port: int = 0
    server_steam_id: int = 0

    sourcetv_server_port: int = 0
    sourcetv_server_name: str = ""

    server_tags: str = ""
    game_id: int = 0
