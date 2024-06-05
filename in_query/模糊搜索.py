import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from datetime import datetime
from jieba.analyse import ChineseAnalyzer  # 导入中文分词器
from fuzzychinese import FuzzyChineseMatch  # 导入 FuzzyChineseMatch
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from whoosh.index import open_dir
from whoosh.query import And
from whoosh import qparser
import string

def preprocess_text(text):
    # Remove punctuation and whitespace, replace with empty string
    cleaned_text = ''.join([char if char not in string.punctuation + string.whitespace else '' for char in text])
    return cleaned_text

def create_search_index(data, index_dir):
    # 定义模式
    schema = Schema(id=ID(stored=True, unique=True), title=TEXT(stored=True, analyzer=ChineseAnalyzer()),
                    content=TEXT(stored=True, analyzer=ChineseAnalyzer()), time=NUMERIC(stored=True))  # 添加了时间字段的定义

    # 如果索引目录不存在，则创建
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)

    # 创建索引
    ix = create_in(index_dir, schema)

    writer = ix.writer()

    for i, item in enumerate(data, start=1):
        # 对文本进行预处理
        processed_title = preprocess_text(item['title'])
        processed_content = preprocess_text(item['content'])
        writer.add_document(id=str(i), title=processed_title, content=processed_content, time=item['time'])  # 修改为使用时间字段

    writer.commit()
    print(f"Index created in {index_dir}")

    # 打印预处理后的文本内容
    print("Preprocessed text for training Fuzzy Chinese Match model:")
    for doc in data:
        print("Title:", preprocess_text(doc['title']))
        print("Content:", preprocess_text(doc['content']))
        print()




def search_keywords(keywords, index_dir):
    ix = open_dir(index_dir)
    # 创建 FuzzyChineseMatch 实例
    fcm = FuzzyChineseMatch(ngram_range=(1, 3), analyzer='stroke')  # 使用适当的参数

    # 拟合模型
    with ix.searcher() as searcher:
        # 获取所有文档的内容字段，并进行预处理
        test_dict = [preprocess_text(hit['content']) for hit in searcher.all_stored_fields()]

        # 训练模型
        fcm.fit(test_dict)

        # 将查询关键字转换为模糊匹配的结果
        flattened_keywords = [preprocess_text(word) for word in keywords]
        fuzzy_keywords = fcm.transform(flattened_keywords)  # 将关键字列表展开后传递给 transform 方法

        # 创建一个解析器，可以解析content字段
        parser = MultifieldParser(["content", "title"], ix.schema, group=qparser.OrGroup.factory(0.9))  # 使用OrGroup，并设置奖励因子

        # 添加模糊搜索插件
        parser.add_plugin(qparser.FuzzyTermPlugin())

        # 构建查询语句
        query_string = ' OR '.join([f'content:"{word}"' for word in fuzzy_keywords])
        query = parser.parse(query_string)

        # 执行查询
        hits = searcher.search(query)

        # 将搜索结果转换为字典列表
        results = [{"id": hit['id'], "title": hit['title'], "time": hit['time']} for hit in hits]

    return results



if __name__ == "__main__":
    data = [
        {"title": "你好啊！小朋友", "content": "我是一个人.", "time": datetime(2024, 5, 1).timestamp()},
        {"title": "Document 2", "content": "我是两个人", "time": datetime(2024, 5, 2).timestamp()},
        {"title": "Document 3", "content": "我是三个人", "time": datetime(2024, 5, 3).timestamp()}
    ]

    index_dir = "indexdir"
    create_search_index(data, index_dir)

    query = input("Enter search terms: ")
    print("Search query:", query)  # 添加打印语句，检查搜索关键字是否正确

    # 执行搜索
    results = search_keywords(query, index_dir)

    # 打印搜索结果
    if results:
        print("Search in content and title:")
        for result in results:
            print("ID:", result['id'], "Title:", result['title'], "Time (Timestamp):", result['time'])
    else:
        print("No matching documents found.")
