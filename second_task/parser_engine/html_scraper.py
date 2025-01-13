import requests
from bs4 import BeautifulSoup


def get_html(page_url):
    page = requests.get(page_url).text
    soup = BeautifulSoup(page, 'lxml')
    return soup


def get_xls(page_url):
    next_page_url = page_url

    while next_page_url:
        soup = get_html(next_page_url)
        results = soup.find_all('a', string='Бюллетень по итогам торгов в Секции «Нефтепродукты»')
        for result in results:
            link = result.get('href')
            year = int(str(link).split('_')[-1][:4])
            if year > 2022:
                yield f'https://spimex.com{link}'
            else:
                break

        new_tag = soup.find("li", class_="bx-pag-next").find('a')
        if new_tag is not None:
            next_page_url = f'https://spimex.com{new_tag.get("href")}'
        else:
            next_page_url = None
