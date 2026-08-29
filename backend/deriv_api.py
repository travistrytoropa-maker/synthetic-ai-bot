import asyncio
import json
import websockets


DERIV_WS_URL = "wss://ws.binaryws.com/websockets/v3"


async def get_active_symbols():
    """
    Get currently available Deriv markets.
    No authentication is required.
    """

    async with websockets.connect(DERIV_WS_URL) as websocket:

        request = {
            "active_symbols": "brief",
            "req_id": 1
        }

        await websocket.send(json.dumps(request))

        response = await websocket.recv()

        data = json.loads(response)

        if data.get("msg_type") == "active_symbols":
            return data.get("active_symbols", [])

        return []


async def get_tick(symbol):
    """
    Get one live tick for a Deriv symbol.
    """

    async with websockets.connect(DERIV_WS_URL) as websocket:

        request = {
            "ticks": symbol,
            "subscribe": 0,
            "req_id": 2
        }

        await websocket.send(json.dumps(request))

        response = await websocket.recv()

        data = json.loads(response)

        if data.get("msg_type") == "tick":

            tick = data.get("tick", {})

            return {
                "symbol": tick.get("symbol"),
                "price": tick.get("quote"),
                "epoch": tick.get("epoch")
            }

        return None


async def stream_ticks(symbol):
    """
    Continuously stream live prices for a symbol.
    """

    async with websockets.connect(DERIV_WS_URL) as websocket:

        request = {
            "ticks": symbol,
            "subscribe": 1,
            "req_id": 3
        }

        await websocket.send(json.dumps(request))

        while True:

            response = await websocket.recv()

            data = json.loads(response)

            if data.get("msg_type") == "tick":

                tick = data.get("tick", {})

                yield {
                    "symbol": tick.get("symbol"),
                    "price": tick.get("quote"),
                    "epoch": tick.get("epoch")
                }


async def test_connection():

    symbols = await get_active_symbols()

    print("Deriv connection successful.")

    print("Markets received:", len(symbols))

    for market in symbols[:10]:

        symbol = market.get("underlying_symbol")
        name = market.get("underlying_symbol_name")

        print(symbol, "-", name)


if __name__ == "__main__":

    asyncio.run(test_connection())