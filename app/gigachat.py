import requests
import json
from app.settings import ENV_PATH
from dotenv import load_dotenv
import os

load_dotenv(ENV_PATH)

url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

payload = 'scope=GIGACHAT_API_PERS'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': f'{os.getenv("GIGA_USER_ID")}',
    'Authorization': f'Basic {os.getenv("GIGA_KEY")}'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

access = response.json()['access_token']

url_m = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"


def generate_text(u_input):
    payload_g = json.dumps({
        "model": "GigaChat-2",
        "messages": [{"role": "system",
                      "content": "Ты гопник c района, который обозревает новости. Тебе отправляют HTML код и твоя задача вытащить от туда информацию и вывести её в стиле гопника в удобном для чтения виде"},
                     {"role": "user",
                      "content": u_input}],
        "stream": False,
        "update_interval": 0
    })
    headers_g = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access}'
    }

    response_g = requests.request("POST", url_m, headers=headers_g, data=payload_g, verify=False)
    return response_g.text


if __name__ == "__main__":
    inp = """
    [<article itemprop="articleBody">
<h1 itemprop="headline">На выборах в Армении у оппозиции есть шанс обойти партию Пашиняна в случае объединения</h1>
<p>Москва. 5 июня. INTERFAX.RU - Участвующие в парламентских выборах Армении оппозиционные партии в случае объединения смогут получить больше голосов, чем партия власти, показал опрос, проведенный армянским представительством GALLUP International Association.</p>
<p>За партию премьер-министра Никола Пашиняна "Гражданский договор" готовы проголосовать 32,4% опрошенных. За партию российского бизнесмена армянского происхождения, главы ГК "Ташир" Самвела Карапетяна "Сильная Армения" - 16,4%, за блок "Армения" экс-президента страны Роберта Кочаряна - 15,2%, за партию "Процветающая Армения" крупного бизнесмена Гагика Царукяна - 8,8%, за партию "Крылья единства" бывшего омбудсмена Армана Татояна - 6,2%.</p>
<p>Таким образом, в сумме четыре основные оппозиционные силы смогут набрать 46,6% голосов.</p>
<p>Намерены голосовать 76,7% респондентов, и 54,6% считают, что выборы пройдут справедливо.</p>
<p>Парламентские выборы пройдут 7 июня, по их итогам будет определен будущий глава правительства.</p>
<div class="h" itemprop="author" itemscope="" itemtype="https://schema.org/Organization">
<meta content="Интерфакс" itemprop="name"/>
<link content="https://www.interfax.ru" itemprop="url" rel="url">
</link></div>
<link href="https://www.interfax.ru/aspimg/1094215.jpg" itemprop="image" rel="image">
<meta content="https://www.interfax.ru/world/1094215" itemprop="mainEntityOfPage"/>
<meta content="2026-06-05T13:29:00+03:00" itemprop="datePublished"/>
<meta content="2026-06-05T13:25:00+03:00" itemprop="dateModified"/>
<div class="h" itemprop="publisher" itemscope="" itemtype="https://schema.org/Organization">
<div itemprop="logo" itemscope="" itemtype="https://schema.org/ImageObject">
<link href="https://www.interfax.ru/img/logo200.png" itemprop="url" rel="url">
<link href="https://www.interfax.ru/img/logo200.png" itemprop="thumbnail" rel="thumbnail">
<meta content="200" itemprop="width"/>
<meta content="60" itemprop="height"/>
</link></link></div>
<meta content="Интерфакс" itemprop="name"/>
<link href="https://www.interfax.ru" itemprop="url" rel="url">
</link></div>
</link></article>]
    """
    print(generate_text(inp))
