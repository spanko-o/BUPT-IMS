from sqlmodel import SQLModel
from database.db import engine
from database.models.user import User


def initialize_database():
    SQLModel.metadata.create_all(engine)
