import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, DATETIME
from whoosh.analysis import RegexTokenizer, LowercaseFilter, StopFilter
from jieba.analyse import ChineseAnalyzer
from database.db import get_session
from database.models.news import News
from sqlmodel import select
from langdetect import detect  # 语言检测库

def create_search_index_from_mysql(index_dir):
    """从数据库中搜索条目写出索引"""
    try:
        with get_session() as session:
            statement = select(News).order_by(News.time)
            results = session.exec(statement).all()

        schema = Schema(
            id=ID(stored=True, unique=True),
            title=TEXT(stored=True, analyzer=ChineseAnalyzer()),  # 默认中文
            content=TEXT(stored=True, analyzer=ChineseAnalyzer()),  # 默认中文
            time=DATETIME(stored=True),
            click_num=TEXT(stored=True),
            url=TEXT(stored=True)
        )

        if not os.path.exists(index_dir):
            os.makedirs(index_dir)

        ix = create_in(index_dir, schema)
        writer = ix.writer()

        for item in results:
            # 检测内容语言
            language = detect(item.title)
            if language == 'zh-cn':  # 中文
                analyzer = ChineseAnalyzer()
            else:  # 假设其他语言使用简单的英文分析器
                analyzer = RegexTokenizer() | LowercaseFilter() | StopFilter()

            writer.add_document(
                id=str(item.id),
                title=item.title,
                url=item.url,
                content=item.content,
                time=item.time,
                click_num=str(item.click_num)
            )

        writer.commit()
        print(f"Index created in {index_dir}")

    except Exception as e:
        print(f"Error: {str(e)}")
        return

def main():
    create_search_index_from_mysql("index_dir")

if __name__ == "__main__":
    main()
