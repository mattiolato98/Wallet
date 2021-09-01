import time

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

from asset_management.models import Asset

API_KEY = "3df992c191bd4ef70ef934d73b2adfe6"
BASE_URL = "https://api.nomics.com/v1/"
HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}


def asset_metadata(symbol):
    parameters = {
        'key': API_KEY,
        'ids': symbol,
    }

    url = BASE_URL + "currencies"

    session = Session()
    session.headers.update(HEADERS)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data[0]['description'], data[0]['logo_url']
    except (ConnectionError, Timeout, TooManyRedirects, IndexError) as e:
        return None, None


def multi_asset_ticker(symbols):
    url = f"{BASE_URL}currencies/ticker?key={API_KEY}&ids={','.join(str(symbol) for symbol in symbols)}"

    session = Session()
    session.headers.update(HEADERS)

    try:
        response = session.get(url)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e



# def prova():
#     start_time = time.time()
#     assets = Asset.objects.all()
#     a = [asset.symbol for asset in assets]
#     b = a[:2020]
#     data = multi_asset_ticker(b)
#     count = 0
#     for asset in data:
#         count += 1
#         print(asset['name'])
#
#     elapsed = time.time() - start_time
#     print(f"\n{count}")
#     print(f"\n{elapsed}")
#
#
# if __name__ == '__main__':
#     prova()