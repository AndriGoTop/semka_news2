from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import requests
from bs4 import BeautifulSoup


def parse_news(source: str, minutes_delta: int = 30, limit: int = 5):
    res = []
    # if source == "interfax":
    #     url_interfax = 'https://www.interfax.ru'
    #     response_interfax = requests.get(url_interfax)
    #     data_interfax = BeautifulSoup(response_interfax.text, 'html.parser')
    #     raw_news_interfax = data_interfax.find_all('div', class_=[
    #         "timeline__group",
    #         'timeline__text',
    #         'timeline__smalltext'], limit=limit)
    #
    #     go = True
    #     msk_tz = ZoneInfo("Europe/Moscow")
    #
    #     for raw_news in raw_news_interfax:
    #         for a in raw_news.find_all('a'):
    #             url_article = f"https://www.interfax.ru{a.get('href')}"
    #             response_article = requests.get(url_article)
    #             data_article = BeautifulSoup(response_article.text, 'html.parser')
    #             raw_article = data_article('article', itemprop="articleBody")
    #             if raw_article:
    #                 date_published_r = raw_article[0].find_all('meta', itemprop='datePublished')[0].get('content')
    #                 date_published_aware = datetime.fromisoformat(date_published_r).replace(tzinfo=msk_tz)
    #
    #                 if date_published_aware > datetime.now(msk_tz) - timedelta(minutes=minutes_delta):
    #                     res.append([raw_article[0], date_published_aware])
    #                 else:
    #                     go = False
    #                     break
    #         if not go:
    #             break

    if source == "rozetked":
        url = "https://rozetked.me/news"
        urls = []
        response = BeautifulSoup(requests.get(url).text, 'html.parser')

        for h2 in response.find_all('h2', class_='title-2 article-preview__title', limit=limit):
            for links in h2.find_all('a'):
                urls.append(links.get('href'))

        for u in urls:
            r = BeautifulSoup(requests.get(u).text, 'html.parser')
            raw_time = r.find_all('time', class_='article__date datum')[0].get('data-datum')
            published_time = datetime.strptime(raw_time, '%Y-%m-%d %H:%M:%S')
            if published_time > datetime.now() - timedelta(minutes=minutes_delta):
                for parag in r.find_all('div', class_='n_main__content'):
                    res.append([parag, published_time])
            else:
                break
    return res


if __name__ == "__main__":
    # print(parse_news('rozetked', 120))
    print(parse_news('rozetked', limit=2, minutes_delta=200000))
