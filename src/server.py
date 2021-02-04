#!/usr/bin/python3

import ssl
import pathlib
import asyncio

import websockets

PORT = 0xf00d


async def handshake(websocket, path):
    print("Connection established.")
    assert await websocket.recv() == 'client'
    await websocket.send('server')
    print("Connection terminated.")


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
certfile = pathlib.Path(__file__).with_name("cert.pem")
keyfile = pathlib.Path(__file__).with_name("key.pem")
ssl_context.load_cert_chain(certfile, keyfile)

start_server = websockets.serve(
    handshake, "0.0.0.0", PORT, ssl=ssl_context
)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
