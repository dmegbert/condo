from bs4 import BeautifulSoup
import requests


def get_page_content(url, headers=None, **url_params):
    if url_params:
        url_suffix = '&'.join([f'{k}={v}' for k, v in url_params.items()])
        url = f'{url}?{url_suffix}'
    resp = requests.get(url, headers=headers)
    return BeautifulSoup(resp.content, 'html.parser')
