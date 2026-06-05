from sqlalchemy import create_engine
from app.settings import POSTGRES_PATH
from app.models import Base

engine = create_engine(
    POSTGRES_PATH,
    echo=True
)

Base.metadata.create_all(engine)
