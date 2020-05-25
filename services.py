import requests
from settings import FINNHUB_TOKEN
from datetime import datetime, timedelta


def finnhub_connection(period=None, ticker=None):
    url = 'https://finnhub.io/api/v1/calendar/earnings'
    params = {
        'from': datetime.now().date(),
        'to': datetime.now().date() + timedelta(days=period),
        'symbol': ticker,
        'token': FINNHUB_TOKEN
    }
    response = requests.get(url=url, params=params)
    return response.text
