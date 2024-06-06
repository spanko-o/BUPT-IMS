from sqlmodel import create_engine, Session
from settings import get_config

config = get_config()

DATABASE_URL = (f"mysql+mysqlconnector://{config.get('DB_USER')}:{config.get('DB_PASSWORD')}@{config.get('DB_HOST')}"
                f"/{config.get('DB_NAME')}")
engine = create_engine(DATABASE_URL)


def get_session():
    return Session(engine)
