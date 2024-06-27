import json
import time

from tornado import websocket as tws

async def create_websocket_stream(endpoint, data_holder):
    messages_this_sec = 0
    this_sec = 0
    client = await tws.websocket_connect(endpoint)
    while True:
        data = await client.read_message()
        messages_this_sec += 1
        if int(time.time()) > this_sec:
            this_sec = int(time.time())
            print("messages this second", messages_this_sec)
            messages_this_sec = 0
        data = json.loads(data)["data"]
        data_holder[data["s"]] = (float(data["b"]), float(data["a"]))


