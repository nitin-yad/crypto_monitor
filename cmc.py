import json

from os import path
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from utils import chunker

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'ad9fb38c-96bc-4b32-8d32-b7ec7def1101',
}

session = Session()
session.headers.update(headers)


def get_top_n_cmc(n):
    list_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': n,
        'convert': 'USD'
    }
    ids = []
    try:
        resp = session.get(list_url, params=parameters)
        dt = json.loads(resp.text)
        for detail in dt['data']:
            print("id: " + detail['id'].__str__() + ", name: " + detail['name'])
            ids.append(detail['id'])
    except (ConnectionError, Timeout, TooManyRedirects, Exception) as e:
        print(e)
    return ids


def get_twitter_name_from_ids(cmc_ids):
    info_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
    tw_ids = []
    for id_chunk in list(chunker(cmc_ids, 500)):
        try:
            info_parameters = {
                'id': ','.join(map(str, id_chunk))
            }
            response = session.get(info_url, params=info_parameters)
            data = json.loads(response.text)
            for i in data['data'].keys():
                print(data['data'][i])
                twitter = data['data'][i]['urls']['twitter']
                if twitter:
                    d = twitter[0].split('/')
                    tw_id = d[len(d) - 1]
                    tw_ids.append(tw_id.__str__())
        except (ConnectionError, Timeout, TooManyRedirects, Exception) as e:
            print(e)
    return tw_ids


def write_to_file(ids):
    f = open("twitter_names.txt", "a+")
    for o in ids:
        f.write('%s\n' % o)
    f.close()


def get_twitter_names():
    names = []
    if path.exists("twitter_names.txt"):
        f = open("twitter_names.txt", "r+")
        for line in f:
            c = line[:-1]
            names.append(c)
        f.close()
        return names
    else:
        cmc_ids = get_top_n_cmc(1500)
        twitter_names = get_twitter_name_from_ids(cmc_ids)
        write_to_file(twitter_names)
        return twitter_names


if __name__ == "__main__":
    t_names = get_twitter_names()

    for t in list(chunker(t_names, 100)):
        if t.__contains__("aeternity"):
            print(t)
