import asyncio
import websockets
import json

from influxdb.setup import write_to_influxdb


# https://binance-docs.github.io/apidocs/futures/en/#mark-price-stream
async def call_mark_price():
    async with websockets.connect(
        "wss://fstream.binance.com/ws/ethusdt@markPrice/btcusdt@markPrice/bnbusdt@markPrice"
    ) as ws:
        while True:
            response = await asyncio.wait_for(ws.recv(), timeout=11)
            response = json.loads(response)
            data = {
                "symbol": response["s"],
                "price": response["p"],
                "timestamp": response["E"],
            }
            # print({"symbol":response["s"],"price":response["p"], "timestamp": response["E"]})
            write_to_influxdb(data)
            # print("wrote to influxdb", data)
            await asyncio.sleep(0.5)


asyncio.get_event_loop().run_until_complete(call_mark_price())
