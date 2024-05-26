import socket

import a2s_query as query

server_addr = "2.56.188.142", 10313
s = socket.socket(type=socket.SOCK_DGRAM)
s.connect(server_addr)

s.sendto(
    query.A2SPacket(
        query.A2SPacketType.A2S_INFO, payload=b"Source Engine Query\0"
    ).pack(),
    server_addr,
)

while True:
    data, addr = s.recvfrom(1024)
    packet = query.A2SPacket.unpack(bytearray(data))

    if not packet:
        print(data)
        break

    if packet.split_type == query.SplitType.SPLIT:
        print("uhh yeah no.")
        break

    if packet.type == query.A2SPacketType.S2C_CHALLENGE:
        packet.type = query.A2SPacketType.A2S_INFO
        packet.payload = b"Source Engine Query\0"

        s.sendto(packet.pack(), server_addr)

    if packet.type == query.A2SPacketType.A2S_INFO_RESPONSE:
        print(packet.parse_payload())
        break
