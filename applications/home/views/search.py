from applications.base import APIView
from middleware.exceptions import BadRequestException
from middleware.exception_catcher import exception_catcher
from middleware.token_authentication import verify_token
from applications.home.utils.query import query_results
from applications.home.utils.timestamp_trans import timestamp_to_date


class SearchAPIView(APIView):
    @verify_token
    @exception_catcher
    def get(self, search, page=1):
        index_dir = 'index_dir'
        results = query_results(search, page, index_dir)

        if not results:
            raise BadRequestException(f'No news found for search term: {search}')

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
            'search': search,
            'len': len(temp_list),
            'page': page,  # 当前页码
            'results': temp_list
        }

        # 返回包含新闻列表的响应
        self.response_utils.ok(self.handler, result_dict)