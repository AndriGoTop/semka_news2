from fastapi import FastAPI
from pydantic import BaseModel
from app.db import engine
from app.models import Test
from sqlalchemy.orm import Session

app = FastAPI()


class TestScheme(BaseModel):
    name: str
    fullname: str | None


@app.post("/posts", tags=['Посты'])
def test_def(data: TestScheme):
    with Session(engine) as session:
        post = Test(
            name=data.name,
            fullname=data.fullname,
        )
        session.add(post)
        session.commit()
    return {"M": "Hello, world"}
