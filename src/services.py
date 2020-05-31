import requests
from settings import FINNHUB_TOKEN
from datetime import datetime, timedelta


class FunnhubService:

    def __init__(self):
        self.url = 'https://finnhub.io/api/v1/'

    def get_earnings(self, period=None, ticker=None):
        url = self.url + 'calendar/earnings'
        params = {
            'from': datetime.now().date(),
            'to': datetime.now().date() + timedelta(days=period),
            'symbol': ticker,
            'token': FINNHUB_TOKEN
        }
        response = requests.get(url=url, params=params)
        return response.text

    def get_name_by_ticker(self, ticker):
        url = self.url + 'stock/profile2'
        params = {
            'symbol': ticker,
            'token': FINNHUB_TOKEN
        }
        response = requests.get(url=url, params=params)
        return response.text
