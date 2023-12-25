import asyncio
import websockets
import json

from utils import write_to_influxdb


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
            write_to_influxdb(data)
            await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(call_mark_price())