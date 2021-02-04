#!/usr/bin/python3

import asyncio
import websockets

PORT = 0xf00d


async def handshake(websocket, path):
    print("Connection established.")
    assert await websocket.recv() == 'client'
    await websocket.send('server')
    print("Connection terminated.")


start_server = websockets.serve(handshake, "0.0.0.0", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
