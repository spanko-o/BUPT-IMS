from applications.base import APIView
from middleware.exceptions import BadRequestException
from middleware.exception_catcher import exception_catcher
from middleware.token_authentication import auth_required
from applications.home.utils.query import query_results
from applications.home.utils.timestamp_trans import timestamp_to_date
from urllib.parse import urlparse, parse_qs
from middleware.responses import ResponseUtils
from middleware.json_utils import JSONUtils
import json
class SearchAPIView(APIView):
    def __init__(self, handler):
        super().__init__(handler)

    @exception_catcher
    @auth_required

    def post(self):
        # 使用 JSONUtils 解析 JSON 数据
        try:
            request_body = JSONUtils.parse_json(self.handler)
        except BadRequestException as e:
            raise BadRequestException('Invalid JSON data in request body')

        # 获取请求体中的参数
        search_term = request_body.get('keywords', '')  # 获取 'keywords' 参数
        page = int(request_body.get('page', 1))  # 获取 'page' 参数，默认值为 1

        # 验证获取的参数
        if not search_term:
            raise BadRequestException('Missing search term (keywords)')

        # 执行搜索逻辑
        index_dir = 'index_dir'  # 替换为你的索引目录
        results = query_results(search_term, page, index_dir)

        if not results:
            raise BadRequestException(f'No news found for search term: {search_term}')

        temp_list = []
        for result in results:
            temp_dict = {
                "id": result['id'],
                "title": result['title'],
                'url': result['url'],
                "time": timestamp_to_date(result['time']),
                "click_num": result['click_num']
            }
            temp_list.append(temp_dict)

        result_dict = {
            'search': search_term,
            'len': len(temp_list),
            'page': page,  # 当前页码
            'results': temp_list
        }

        # 返回包含搜索结果的响应
        ResponseUtils.ok(self.handler, result_dict)
