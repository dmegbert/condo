from bs4 import BeautifulSoup
import requests

from utils import get_page_content


iw_condos_url = 'https://www.rinconrealestateforsale.com/Rincon_Condominiums/page_2690646.html'


def main():
    page = get_page_content(iw_condos_url)
    condos = _get_condos(page)
    print(condos)


def _get_condos(page):
    condos = []
    for condo_div in page.find_all('div', class_='listview-item-cnt'):
        condo = {}
        condo = _get_condo_url(condo, condo_div)
        condo = _get_condo_price(condo, condo_div)
        condo = _get_condo_photo(condo, condo_div)
        condo = _get_bathrooms_and_bedrooms(condo, condo_div)
        condos.append(condo)
    return condos


def _get_condo_url(condo, condo_div):
    url_elem = condo_div.find('div', class_='item-address')
    condo['url'] = url_elem.find('a').get('href')
    return condo


def _get_condo_price(condo, condo_div):
    price_div = condo_div.find('div', class_='item-price')
    for price_span in price_div('span'):
        price = price_span.string
        if price and '$' in price:
            condo['price'] = price
            break
    return condo


def _get_condo_photo(condo, condo_div):
    photo = condo_div.find('img')
    condo['photo'] = photo.get('src')
    return condo


def _get_bathrooms_and_bedrooms(condo, condo_div):
    spans = condo_div('span')
    condo['bedrooms'] = 0
    condo['bathrooms'] = 0
    for idx, span in enumerate(spans):
        if span.string == 'Bathrooms':
            condo['bathrooms'] = spans[idx+1].string
        if span.string == 'Bedrooms':
            condo['bedrooms'] = spans[idx+1].string
    return condo


if __name__ == '__main__':
    main()
