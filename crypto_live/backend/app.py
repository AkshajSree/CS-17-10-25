from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Import the robust fetch_prices_with_retry function from prices_html
from backend import prices_html

app = FastAPI()

@app.get("/")
def root():
    try:
        prices = prices_html.fetch_prices_with_retry()  # Fetch latest prices with retry logic
        # Convert datetime objects to ISO format string for JSON serialization
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
        # Return HTTP 500 with error details
        return JSONResponse(status_code=500, content={"error": str(e)})
