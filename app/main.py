import datetime
from fastapi import FastAPI, status
from app.db import engine
from app.models import News
from sqlalchemy.orm import Session
from app.schemas import NewsScheme, ParsingSchemas
from app.paprsing import parse_news
from app.gigachat import generate_text
from sqlalchemy import select
import re

app = FastAPI()


@app.post("/news/create", tags=['Посты'])
def create_post(data: NewsScheme):
    with Session(engine) as session:
        post = News(
            heading=data.heading,
            article=data.article,
            created_at=data.created_at,
        )
        session.add(post)
        session.commit()
    return post


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


