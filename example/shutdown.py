#!/usr/bin/env python

import asyncio
import signal
import websockets

async def echo(websocket, path):
    while True:
        try:
            msg = await websocket.recv()
        except websockets.ConnectionClosed:
            pass
        else:
            await websocket.send(msg)

loop = asyncio.get_event_loop()

# Create the server.
start_server = websockets.serve(echo, 'localhost', 8765)
server = loop.run_until_complete(start_server)

# Run the server until SIGTERM.
stop_server = asyncio.Future()
loop.add_signal_handler(signal.SIGTERM, stop_server.set_result, None)
loop.run_until_complete(stop_server)

# Shut down the server.
server.close()
loop.run_until_complete(server.wait_closed())
