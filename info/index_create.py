import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from datetime import datetime
from jieba.analyse import ChineseAnalyzer
from whoosh.analysis import StemmingAnalyzer  # 导入StemmingAnalyzer

import pymysql.cursors

def create_search_index_from_mysql(db_host, db_user, db_password, db_name, db_port, table_name, index_dir):
    """从数据库中搜索条目写出索引
    : param db_host:数据库的主机
    : param db_user: 数据库用户名
    : param db_password:数据库密码
    ：param db_name 数据库的名字
    : param db-port 端口
    : param table_name 数据库表名字
    : param index_dir 索引所在的位置

    """

    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        port=db_port,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()


        schema = Schema(
            id=ID(stored=True, unique=True),
            title=TEXT(stored=True, analyzer=ChineseAnalyzer()),  # 使用ChineseAnalyzer处理中文
            content=TEXT(stored=True, analyzer=StemmingAnalyzer()),  # 使用StemmingAnalyzer处理英文
            time=NUMERIC(stored=True)
        )


        if not os.path.exists(index_dir):
            os.makedirs(index_dir)


        ix = create_in(index_dir, schema)
        writer = ix.writer()


        for item in data:

            timestamp = int(item['timestamp'].timestamp())

            writer.add_document(id=str(item['id']), title=item['title'], content=item['txt'], time=timestamp)

        writer.commit()
        print(f"Index created in {index_dir}")

    finally:
        connection.close()


if __name__ == '__main__':
    db_host = 'localhost'
    db_user = 'root'
    db_password = 'Y1j1i1123'
    db_name = 'python_database'
    db_port = 3306
    table_name = 'message'
    index_dir = "indexdir"

    create_search_index_from_mysql(db_host, db_user, db_password, db_name, db_port, table_name, index_dir)
