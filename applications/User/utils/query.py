from whoosh.qparser import MultifieldParser
from whoosh.index import open_dir
from whoosh.query import Or,And
import string
from whoosh import qparser
def search_keywords(keywords:list, index_dir:string, page_num:int, results_per_page=1):
    """进行信息检索：
    param keywords：列表，index_dir索引目录，page_num要求的页码数
    param index_dir 索引目录
    param page_num :web页数点击指定页数返回的结果

    返回列表形式
    """
    ix = open_dir(index_dir)
    # 创建一个解析器，可以解析content和title字段
    parser = MultifieldParser(["content", "title"], ix.schema, group=qparser.OrGroup.factory(0.9))  # 使用OrGroup，并设置奖励因子

    # 添加模糊搜索插件
    parser.add_plugin(qparser.FuzzyTermPlugin())

    # 构造 And 组合子查询，确保搜索结果必须包含所有关键字
    query = And([parser.parse(keyword) for keyword in keywords])

    # 存储搜索结果的列表
    results = []
    with ix.searcher() as searcher:
        # 设置按时间戳字段降序排序
        hits = searcher.search_page(query, page_num, pagelen=results_per_page, sortedby="time", reverse=True)

        # 如果请求的页数超过了可用页数，则不返回任何结果
        if page_num > hits.pagecount:
            return results

        for hit in hits:
            # 将时间字段转换为时间戳
            time_stamp = hit["time"]
            results.append({"id": hit["id"], "title": hit["title"], "time": time_stamp})

    return results

def query_keywords(query:string):
    '''对query字符串进行处理
    param query：被检索的字符串
    返回一个关键词列表'''
    keywords = [char for char in query if char not in string.punctuation]
    # 将查询字符串拆分为单词列表
    keywords = "".join(keywords).split()
    return keywords


if __name__ == "__main__":
    query = input("输入搜索词: ")
    page_num = int(input("输入页码: "))

    # 去除标点符号并将查询字符串拆分为单个关键字的列表
    keywords = query_keywords(query)

    print("在内容和标题中搜索:")
    results = search_keywords(keywords, 'indexdir', page_num)
    for result in results:
        print("ID:", result['id'], "标题:", result['title'], "时间 (时间戳):", result['time'])
