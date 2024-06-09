from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime
from sqlalchemy import Text


class News(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # 主键
    title: str = Field(sa_column_kwargs={"nullable": False, "unique": True}, max_length=255)  # 标题，最大长度255字符
    url: str = Field(sa_column_kwargs={"nullable": False, "unique": True})  # URL，必须字段且唯一
    department: str = Field(sa_column_kwargs={"nullable": False}, max_length=40)  # 部门，最大长度40字符
    time: datetime = Field(sa_column_kwargs={"nullable": False})  # 时间，使用 datetime 类型
    content: str = Field(sa_column=Column(Text, nullable=False))
    chart: Optional[str] = Field(sa_column=Column(Text, nullable=True))
    click_num: int = Field(default=None)
