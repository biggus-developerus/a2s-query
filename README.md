# a2s-query
Simple python implementation of the A2S query protocol 

A2S protocol info [here](https://developer.valvesoftware.com/wiki/Server_queries).

A2S info request
```py
query.A2SPacket(
    query.A2SPacketType.A2S_INFO, 
    payload=b"Source Engine Query\0"
)
```

A2S player request
```py
cnum = int.to_bytes(-1, 4, "little", signed=True) # challenge number (-1 to request one

query.A2SPacket(
    query.A2SPacketType.A2S_PLAYER,
    challenge_number=cnum,
)
```

Unpacking A2S packet
```py
query.A2SPacket.unpack(data)

# Resending request with challenge number
if packet.type == query.A2SPacketType.S2C_CHALLENGE:
    packet.type = query.A2SPacketType.A2S_PLAYER # or A2S_INFO
    s.sendto(packet.pack(), server_addr)
```

# TODO 
- [ ] Pack method for responses (A2SInfoResp & A2SPlayerResp)
- [ ] Net package (allows for sending query responses and requests)
- [ ] Multi-packet Response support (split_type = -2)