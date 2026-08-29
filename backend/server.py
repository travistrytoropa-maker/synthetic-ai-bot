from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from deriv_api import get_active_symbols, get_tick

app = FastAPI(title="Synthetic AI Signal Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Synthetic AI Signal Engine is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/markets")
async def markets():
    symbols = await get_active_symbols()

    markets = []

    for market in symbols:
        markets.append({
            "symbol": market.get("underlying_symbol"),
            "name": market.get("underlying_symbol_name"),
            "display_name": market.get("display_name")
        })

    return {
        "count": len(markets),
        "markets": markets
    }


@app.get("/tick/{symbol}")
async def tick(symbol: str):
    data = await get_tick(symbol)

    if data is None:
        return {
            "status": "error",
            "message": f"No tick received for {symbol}"
        }

    return {
        "status": "success",
        "data": data
    }