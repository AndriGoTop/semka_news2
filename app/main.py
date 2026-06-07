import datetime
from fastapi import FastAPI, status, HTTPException
from app.db import engine
from app.models import News
from sqlalchemy.orm import Session
from app.schemas import NewsScheme, ParsingSchemas, NewsSchemaUpdate
from app.paprsing import parse_news
from app.gigachat import generate_text
from sqlalchemy import select, desc
import re

app = FastAPI()


@app.get('/news', tags=['Посты'])
def get_news(limit: int):
    session = Session(engine)
    stmt = select(News).order_by(desc(News.id)).limit(limit)

    results = session.scalars(stmt).all()
    return_res = [NewsScheme.model_validate(item) for item in results]

    return {'data': return_res}


@app.get('/news/{news_id}', tags=['Посты'])
def get_news_by_id(news_id):
    session = Session(engine)
    stmt = select(News).where(News.id == news_id)
    results = session.scalars(stmt).one_or_none()
    if results is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # Или просто написать 404
            detail=f"Элемент с id {news_id} не найден"
        )
    return_res = NewsScheme.model_validate(results)
    return {'data': return_res}


@app.put('/news/{news_id}', tags=["Посты"])
def update_all_data_news(data: NewsScheme, news_id: int):
    session = Session(engine)
    stmt = select(News).where(News.id == news_id)
    results = session.scalars(stmt).one_or_none()
    if results is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # Или просто написать 404
            detail=f"Элемент с id {news_id} не найден"
        )
    results.heading = data.heading
    results.article = data.article
    results.created_at = data.created_at
    session.commit()
    return HTTPException(status_code=status.HTTP_200_OK)


@app.patch('/news/{news_id}', tags=["Посты"], status_code=status.HTTP_200_OK)
def update_some_data_news(data: NewsSchemaUpdate, news_id: int):
    session = Session(engine)
    stmt = select(News).where(News.id == news_id)
    results = session.scalars(stmt).one_or_none()
    if results is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # Или просто написать 404
            detail=f"Элемент с id {news_id} не найден"
        )
    if data.heading is not None:
        results.heading = data.heading
    if data.article is not None:
        results.article = data.article
    if data.created_at is not None:
        results.created_at = data.created_at
    session.commit()
    return HTTPException(status_code=status.HTTP_200_OK, detail='Обновлено успешно')


@app.delete('/news/{news_id}', tags=["Посты"], status_code=status.HTTP_204_NO_CONTENT)
def update_some_data_news(news_id: int):
    session = Session(engine)
    results = session.get(News, news_id)
    print('===', results)
    if results is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # Или просто написать 404
            detail=f"Элемент с id {news_id} не найден"
        )
    session.delete(results)
    session.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='Удалено успешно')


@app.post("/news", tags=['Посты'])
def create_post(data: NewsScheme):
    with Session(engine) as session:
        post = News(
            heading=data.heading,
            article=data.article,
            created_at=data.created_at,
        )
        session.add(post)
        session.commit()
    return {"status": "OK"}


@app.post("/news/parsing", tags=["Посты"], status_code=200)
def parsing_news(param: ParsingSchemas):
    parsed_news = parse_news(source=param.source, limit=param.limit, minutes_delta=param.minutes_delta)

    for n in parsed_news:
        with Session(engine) as session:
            a = select(News).where(News.created_at == n[1])
            if session.scalar(a) is None:
                ai_gener = generate_text(str(n[0]))["choices"][0]['message']["content"]
                title = re.search(r"^\[TITLE\]:\s*(.*?)$", ai_gener, re.MULTILINE).group(1)
                body = re.search(r"^\[BODY\]:\s*([\s\S]+)$", ai_gener, re.MULTILINE).group(1).strip()

                post = News(
                    heading=title,
                    article=body,
                    created_at=n[1]
                )
                session.add(post)
                session.commit()
    return {"status": "OK"}
