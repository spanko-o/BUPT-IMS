from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True, max_length=8)
    username: str = Field(index=True)
    phone: str = Field(default=None, index=True)
    password: str
