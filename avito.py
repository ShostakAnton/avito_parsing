import requests
from bs4 import BeautifulSoup
import csv

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}  # имуляция действия поведения браузера


def get_html(url):
    session = requests.Session()  # непрерывность действия во времени (имитация человека)
    request = session.get(url, headers=headers)  # имуляция открытия странички в браузере
    soup = BeautifulSoup(request.content, 'lxml')
    # return soup

    # r = requests.get(url)  # запрос на сервер
    return request.content


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-pages clearfix').find_all('a')[-1].get('href')
    total_page = pages.split('=')[1].split('&')[0]

    return int(total_page)


def write_csv(data):
    with open('avito.csv', 'a') as f:
        write = csv.writer(f)
        write.writerow((data['title'],
                        data['price'],
                        data['metro'],
                        data['url']))


def get_page_date(html):
    soup = BeautifulSoup(html, 'lxml')
    abs = soup.find('div', class_='js-catalog_serp').find_all('div',
                                                              class_="snippet-horizontal item item_table clearfix js-catalog-item-enum item-with-contact js-item-extended")

    for ad in abs:
        name = ad.find('div', class_="description item_table-description").find('h3').text
        if 'HTC' or 'htc' in name:
            try:
                title = ad.find('div', class_="description item_table-description").find('h3').text
            except:
                title = ''
            try:
                price = ad.find('div', class_="description item_table-description").find('div',
                                                                                         class_='snippet-price-row').text
            except:
                price = ''
            try:
                url = 'https://www.avito.ru/' + ad.find('div', class_="description item_table-description").find(
                    'a').get(
                    "href")
            except:
                url = ''

            try:
                metro = ad.find('div', class_="description item_table-description").find('div', class_='data').find(
                    'div',
                    class_='item-address-georeferences').text
                metro = ' '.join(metro.split())
            except:
                metro = ''

            data = {
                'title': title,
                'price': price,
                'metro': metro,
                'url': url,
            }

            write_csv(data)

        else:
            continue


def main():
    url = 'https://www.avito.ru/moskva/telefony?q=htc&p=1'
    base_url = 'https://www.avito.ru/moskva/telefony?q=htc&p='
    # total_pages = get_total_pages(get_html(url))

    for i in range(1, 3):
        url_gen = base_url + str(i)
        # print(url_gen)
        html = get_html(url_gen)
        get_page_date(html)


if __name__ == '__main__':
    main()
