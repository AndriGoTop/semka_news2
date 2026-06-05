from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.settings import POSTGRES_PATH
from app.models import Base, Posts


engine = create_engine(
    POSTGRES_PATH,
    echo=True
)


Base.metadata.create_all(engine)

