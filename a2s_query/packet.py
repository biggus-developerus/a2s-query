__all__ = (
    "Packet",
    "A2SPacket",
)

from typing import Optional, Union

from a2s_query.enums import A2SPacketType, SplitType
from a2s_query.responses import A2SInfoResp, A2SPlayerResp


class Packet:
    @staticmethod
    def unpack(data: bytearray) -> Optional["Packet"]:
        if len(data) < 4:
            return None

        split_type = SplitType(int.from_bytes(data[:4], "little", signed=True))

        if split_type == SplitType.UNKNOWN:
            return None

        return Packet(split_type)

    def __init__(self, split_type: SplitType = SplitType.NOT_SPLIT) -> None:
        self.split_type: SplitType = split_type

    def pack(self) -> bytearray:
        data = bytearray()
        data += self.split_type.to_bytes(4, "little", signed=True)

        return data


class A2SPacket(Packet):
    @staticmethod
    def unpack(data: bytearray) -> Optional["A2SPacket"]:
        packet = Packet.unpack(data)

        if not packet:
            return None

        packet_data = data[4:]
        a2s_packet = A2SPacket(A2SPacketType(packet_data[0]))
        a2s_packet.split_type = packet.split_type

        if a2s_packet.type == A2SPacketType.S2C_CHALLENGE:
            a2s_packet.challenge_number = packet_data[1:]
            a2s_packet.is_challenge = True
        else:
            a2s_packet.payload = packet_data[1:]

        return a2s_packet

    def __init__(
        self,
        packet_type: A2SPacketType,
        payload: Optional[bytes] = None,
        challenge_number: Optional[bytes] = None,
    ) -> None:
        super().__init__(SplitType.NOT_SPLIT)

        self.type: A2SPacketType = packet_type
        self.payload: Optional[bytes] = payload
        self.challenge_number: Optional[bytes] = challenge_number
        self.is_challenge: bool = False

    def pack(self) -> bytearray:
        data = super().pack()

        data += self.type.to_bytes(1, "little")

        if self.payload:
            data += self.payload
        if self.challenge_number:
            data += self.challenge_number

        return data

    def parse_payload(self) -> Union[A2SInfoResp, A2SPlayerResp]:
        if self.type == A2SPacketType.A2S_INFO_RESPONSE:
            return A2SInfoResp.from_packet(self)
        elif self.type == A2SPacketType.A2S_PLAYER_RESPONSE:
            return A2SPlayerResp.from_packet(self)
