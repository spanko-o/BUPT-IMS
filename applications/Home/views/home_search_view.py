from applications.base import APIView
from middleware.exceptions import BadRequestException
from middleware.exception_catcher import exception_catcher
from middleware.token_authentication import auth_required
from middleware.responses import ResponseUtils
from applications.Home.utils.query import query_results
from applications.Home.utils.timestamp_trans import timestamp_to_date

class SearchAPIView(APIView):

    @exception_catcher
    @auth_required
    def get(self):
        page = self.query_params.get('page', [1])[0]

        try:
            page = int(page)
        except ValueError:
            raise BadRequestException("Invalid page number")
        keyword=self.query_params.get('keyword',[''])[0]
        results=query_results(keyword,page,"index_dir")
        if results is None:
            raise BadRequestException("No news provided")
        temp_list = []
        for result in results:
            temp_dict = {
                "id": result['id'],
                "title": result['title'],
                'url': result['url'],
                "time":result['time'].strftime('%Y-%m-%d %H:%M:%S'),
                 "click_num": int(result['click_num'])
            }
            temp_list.append(temp_dict)

        result_dict = {
            'search': keyword,
            'len': len(temp_list),
            'page': page,  # 当前页码
            'results': temp_list
        }
        ResponseUtils.ok(self.handler, result_dict)




