from whoosh.qparser import MultifieldParser
from whoosh.index import open_dir
from whoosh.query import And
import string
from whoosh import qparser


def search_keywords(keywords, index_dir, page_num, results_per_page=1):
    ix = open_dir(index_dir)
    if not keywords:  # 如果搜索关键词为空，则返回所有数据
        with ix.searcher() as searcher:
            results = []
            for hit in searcher.all_stored_fields():
                results.append({"id": hit["id"], "title": hit["title"], "time": hit["time"],"url": hit["url"]})
        return results

    parser = MultifieldParser(["content", "title"], ix.schema, group=qparser.OrGroup.factory(0.9))
    parser.add_plugin(qparser.FuzzyTermPlugin())
    query = And([parser.parse(keyword) for keyword in keywords])
    results = []
    with ix.searcher() as searcher:
        hits = searcher.search_page(query, page_num, pagelen=results_per_page, sortedby="time", reverse=True)
        if page_num > hits.pagecount:
            return results
        for hit in hits:
            time_stamp = hit["time"]
            results.append({"id": hit["id"], "title": hit["title"], "time": time_stamp,"url": hit["url"],"click_num": hit["click_num"]})
    return results


def query_keyword(query: string):
    keywords = [char for char in query if char not in string.punctuation]
    keywords = "".join(keywords).split()
    return keywords


def query_results(query, page_num, index_dir):
    query_keywords = query_keyword(query)
    results = search_keywords(query_keywords, index_dir, page_num, 10)
    return results
