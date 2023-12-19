from requests import Request, Session


def request(url="https://api.binance.com/api/v3/klines"):
    def _request(symbol, start, end, interval):
        s = Session()
        r = Request

        try:
            request = r(
                "GET",
                url,
                params={
                    "symbol": symbol,
                    "startTime": start,
                    "endTime": end,
                    "interval": interval,
                },
            )
            response = s.send(request.prepare())
            data = response.json()
        except:
            raise
        else:
            return data

    return _request


if __name__ == "__main__":
    binance = request("https://api.binance.com/api/v3/klines")
    res = binance("BTCUSDT", start=1635721200000, end=1635742700000, interval="1m")
    print(len(res))
