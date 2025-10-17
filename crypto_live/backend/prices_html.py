import requests
import time
from datetime import datetime, timezone

def fetch_prices_with_retry(max_retries=3):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    for attempt in range(max_retries):
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            data = r.json()
            print("DEBUG: Raw API response:", data)

            if "bitcoin" in data and "ethereum" in data:
                prices = [
                    {
                        "symbol": "BTC",
                        "price": data["bitcoin"]["usd"],
                        "fetched_at": datetime.now(timezone.utc)
                    },
                    {
                        "symbol": "ETH",
                        "price": data["ethereum"]["usd"],
                        "fetched_at": datetime.now(timezone.utc)
                    }
                ]
                print("DEBUG: Parsed coins count:", len(prices))
                return prices
            else:
                raise ValueError("Missing expected coin data keys.")
        except Exception as e:
            print(f"Fetch attempt {attempt+1} failed: {e}")
            time.sleep(2 ** attempt)
    raise Exception("Failed to fetch prices after maximum retries.")

if __name__ == "__main__":
    try:
        coins = fetch_prices_with_retry()
        for c in coins:
            print(f"{c['symbol']}: ${c['price']} at {c['fetched_at']}")
    except Exception as e:
        print(f"Error fetching prices: {e}")
