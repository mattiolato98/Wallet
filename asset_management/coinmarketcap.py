from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

API_KEY = "502ccb84-fb9f-418a-86fd-bb0f5e41307b"
BASE_URL = "https://pro-api.coinmarketcap.com/"
HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}


def asset_prices(cmc_ids, fiat):
    data = asset_quotes(cmc_ids, fiat)
    return [{'id': cmc_id, 'price': data[f'{cmc_id}']['quote'][fiat]['price']} for cmc_id in cmc_ids]


def asset_quotes(cmc_ids, fiat):
    url = f'{BASE_URL}v1/cryptocurrency/quotes/latest?id={",".join(str(cmc_id) for cmc_id in cmc_ids)}&convert={fiat}'

    session = Session()
    session.headers.update(HEADERS)

    try:
        response = session.get(url)
        data = json.loads(response.text)
        return data['data']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def asset_metadata(cmc_id):
    url = BASE_URL + 'v2/cryptocurrency/info'
    parameters = {
        'id': cmc_id,
    }

    session = Session()
    session.headers.update(HEADERS)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data['data'][f'{cmc_id}']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def asset_list():
    url = BASE_URL + 'v1/cryptocurrency/map'

    session = Session()
    session.headers.update(HEADERS)

    try:
        response = session.get(url)
        data = json.loads(response.text)
        return data['data']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def fiat_list():
    url = BASE_URL + 'v1/fiat/map'

    session = Session()
    session.headers.update(HEADERS)

    try:
        response = session.get(url)
        data = json.loads(response.text)
        return data['data']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def multi_asset_metadata(cmc_ids):
    url = f'{BASE_URL}v2/cryptocurrency/info?id={",".join(str(cmc_id) for cmc_id in cmc_ids)}'

    session = Session()
    session.headers.update(HEADERS)

    try:
        response = session.get(url)
        data = json.loads(response.text)
        return data['data']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e
