from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # Add CORS support

from crypto_live.backend import prices_html

app = FastAPI()

# CORS middleware for allowing connections from frontend server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any origin during local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    try:
        prices = prices_html.fetch_prices_with_retry()
        json_prices = [
            {
                "symbol": coin["symbol"],
                "price": coin["price"],
                "fetched_at": coin["fetched_at"].isoformat()
            }
            for coin in prices
        ]
        return JSONResponse(content={"prices": json_prices})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
