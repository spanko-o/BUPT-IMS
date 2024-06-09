import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, DATETIME
from jieba.analyse import ChineseAnalyzer
from whoosh.analysis import StemmingAnalyzer
from database.db import get_session
from database.models.news import News
from middleware.exceptions import BadRequestException

def create_search_index_from_mysql(index_dir):
    """从数据库中搜索条目写出索引"""
    try:
        with get_session() as session:
            results = session.query(News).order_by(News.time).all()

        schema = Schema(
            id=ID(stored=True, unique=True),
            title=TEXT(stored=True, analyzer=ChineseAnalyzer()),
            content=TEXT(stored=True, analyzer=StemmingAnalyzer()),
            time=DATETIME(stored=True)
        )

        if not os.path.exists(index_dir):
            os.makedirs(index_dir)

        ix = create_in(index_dir, schema)
        writer = ix.writer()

        for item in results:
            writer.add_document(id=str(item.id), title=item.title, content=item.content, time=item.time)

        writer.commit()
        print(f"Index created in {index_dir}")

    except Exception as e:
        return BadRequestException(str(e))