from concurrent.futures import ThreadPoolExecutor, as_completed

from scrapers.utils import get_page_content


def _url(suffix):
    return f'https://www.realestaterinconpr.com/{suffix}'


def get_tropical_condos():
    sitemap = get_page_content(_url('SiteMap.html'))
    condo_urls = _get_rincon_condo_urls(sitemap)
    condos = []

    with ThreadPoolExecutor() as executor:
        future_to_page = {executor.submit(_get_condo_page, url_suffix): url_suffix for url_suffix in condo_urls}
        for future in as_completed(future_to_page):
            url_suffix = future_to_page[future]
            try:
                page = future.result()
                condo = _get_condo(page, url_suffix)
                condos.append(condo)
            except Exception as exc:
                print(exc)
    return condos


def _get_rincon_condo_urls(page):
    condo_urls = []
    for anchor in page('a'):
        url = anchor.get('href', 'no url')
        if 'Condos' in url:
            condo_urls.append(url)
    return condo_urls


def _get_condo_page(url_suffix):
    url = _url(url_suffix)
    return get_page_content(url)


def _get_condo(page, url_suffix):
    condo = {'url': _url(url_suffix), 'price': _get_condo_price(page)}
    condo.update(_get_bathrooms_bedrooms(page))
    condo['photo'] = _get_condo_photo(page)
    return condo


def _get_condo_price(page):
    return page.find(itemprop='price').string


def _get_bathrooms_bedrooms(page):
    bed_baths = {'bathrooms': 0,
                 'bedrooms': 0 }
    details = page.find('div', class_='listing-details-data')
    for li in details.find_all('li', class_='col-sm-6'):
        if li and 'Bedrooms' in str(li):
           bed_baths['bedrooms'] = li.b.string
        if li and 'Bathrooms' in str(li):
            bed_baths['bathrooms'] = li.b.string
    return bed_baths


def _get_condo_photo(page):
    div = page.find('div', id='listing-details-tab')
    for img in div.find_all('img'):
        if img.get('data-src'):
            return img.get('data-src')


if __name__ == '__main__':
    get_tropical_condos()

# data = [
#     {
#         'bathrooms': 0,
#         'bedrooms': 0,
#         'photo': 'full_url',
#         'price': '$392,000',
#         'url': 'ful_url'
#     },
#     {
#         'etc': 0
#     }
# ]
