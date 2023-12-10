import asyncio
import websockets
import json

# https://binance-docs.github.io/apidocs/futures/en/#mark-price-stream

url = "wss://stream.binance.com:9443/ws/btcusdt@markPrice"


import asyncio
import websockets
import json

async def call_mark_price():
    async with websockets.connect("wss://fstream.binance.com/ws/ethusdt@markPrice/btcusdt@markPrice/bnbusdt@markPrice") as ws:
        while True:
            response = await asyncio.wait_for(ws.recv(), timeout=11)
            response=json.loads(response)
            print({"symbol":response["s"],"price":response["p"], "timestamp": response["E"]})
            await asyncio.sleep(0.5)

asyncio.get_event_loop().run_until_complete(call_mark_price())