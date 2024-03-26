import requests

api_url = "https://api.binance.com/api/v3/ticker/price"
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()

    prices = {}

    top_20_pairs = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "SOLUSDT", "ADAUSDT",
                    "DOTUSDT", "LUNAUSDT", "LINKUSDT", "AVAXUSDT", "DOGEUSDT", "LTCUSDT",
                    "MATICUSDT", "ALGOUSDT", "ATOMUSDT", "ICPUSDT", "FILUSDT", "SHIBUSDT",
                    "UNIUSDT", "XMRUSDT"]

    for pair_data in data:
        pair = pair_data['symbol']
        if pair in top_20_pairs:
            symbol = pair.replace("USDT", "")
            prices[symbol] = float(pair_data['price'])

    for symbol, price in prices.items():
        print(f"{symbol}: {price}$")
else:
    print("Ошибка при запросе к API Binance")