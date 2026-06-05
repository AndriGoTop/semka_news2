import requests
import json
from app.settings import ENV_PATH
from dotenv import load_dotenv
import os
import re

load_dotenv(ENV_PATH)


def generate_text(u_input):
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    system_promt = """
    Ты — опытный Backend-парсер данных и одновременно мастер дворового сленга. Твоя задача — обработать полученный HTML-код новостной статьи и вернуть строго структурированный ответ.

    ### ИНСТРУКЦИЯ ПО ОБРАБОТКЕ:
    1. Найди в HTML-коде заголовок новости и текст самой новости. Очисти их от всех HTML-тегов.
    2. Сформулируй заголовок новости.
    3. Перепиши основной текст новости, полностью изменив стиль: это должен быть сочный, каноничный гоп-стоп сленг (используй словечки вроде "короче", "слышь", "пацаны", "тема", "чисто", "мутки", "базар", но без жесткого мата, чтобы не сработали фильтры цензуры). Смысл новости при этом должен остаться понятным.
    
    ### ФОРМАТ ВЫВОДА (ЭТО КРИТИЧЕСКИ ВАЖНО):
    Ты должен вернуть ответ СТРОГО в следующем формате. Не добавляй никаких вводных слов, приветствий или лишних символов вне этой структуры.
    
    [TITLE]: <здесь исходное или слегка адаптированное название новости одной строкой>
    [BODY]:
    <здесь перефразированный в стиле гопника текст новости, можно разбивать на абзацы>
    
    ### ПРИМЕР ВЫВОДА:
    [TITLE]: В зоопарке родился редкий белый кенгуру
    [BODY]:
    Слышь, пацаны, тут чисто тема обрисовывалась в зоопарке. У кенгуру мелкий родился, вообще белый, прикинь? Чисто эксклюзивчик, без базара. На районе таких еще никто не видел.
    
    ### ИСХОДНЫЙ HTML ДЛЯ ОБРАБОТКИ:
    """

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
    payload_g = json.dumps({
        "model": "GigaChat-2",
        "messages": [{"role": "system",
                      "content": system_promt},
                     {"role": "user",
                      "content": u_input},
                     {'role': "user",
                      "content": "Выведи отдельно название новости"}],
        "stream": False,
        "update_interval": 0
    })
    headers_g = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access}'
    }

    response_g = requests.request("POST", url_m, headers=headers_g, data=payload_g, verify=False)
    return response_g.json()


if __name__ == "__main__":
    inp = """
    Привет
    """
    # print(generate_text(str("Ученые изобрели телепорт"))["choices"][0]['message']["content"])
    test_data = """[TITLE]: Учёные изобрели телепорт
[BODY]:
Короче, пацаны, чуваки из науки мутили тему про телепорт. Представляешь себе? Теперь можно будет бабки прямо через экран пересылать! Вот это да, реально тема! Только пока непонятно, как конкретно пользоваться этим делом, ну ты понимаешь... Базарят, что скоро до простых смертных дойдет. Так что следим за развитием событий, хе-хе.
"""
    title = re.search(r"^\[TITLE\]:\s*(.*?)$", test_data, re.MULTILINE).group(1)
    body = re.search(r"^\[BODY\]:\s*([\s\S]+)$", test_data, re.MULTILINE).group(1).strip()

    print("Заголовок:", title)
    print("Текст:", body)
