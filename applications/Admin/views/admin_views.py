from applications.base import APIView
from middleware.exceptions import BadRequestException
from middleware.exception_catcher import exception_catcher
from database.db import get_session
from database.models.news import News
from middleware.token_authentication import auth_required
from middleware.responses import ResponseUtils
from sqlmodel import select
from applications.Admin.utils.News_delete import news_delete
from applications.Admin.utils.visualization import ksh_analysis

class AdminViews(APIView):

    @exception_catcher
    @auth_required
    def get(self, page=1):
        page = self.query_params.get('page', [1])[0]
        page_size = 10  # 每页显示的新闻条目数
        try:
            page = int(page)
        except ValueError:
            raise BadRequestException("Invalid page number")

        with get_session() as session:
            # 计算分页偏移量
            offset = (page - 1) * page_size

            # 查询新闻条目，并应用分页
            statement = select(News).order_by(News.time).offset(offset).limit(page_size)
            results = session.exec(statement).all()
        image=ksh_analysis()
        news_list = []
        for result in results:
            # 提取新闻的必要字段，并将 datetime 对象转换为字符串
            news_dict = {
                "title": result.title,
                "url": result.url,
                "department": result.department,
                "time": result.time.strftime('%Y-%m-%d %H:%M:%S'),
                "click_num": result.click_num
            }
            news_list.append(news_dict)

        result_dict = {
            "news": news_list,
            "len": len(news_list),  # 当前页新闻的条目数
            "page": page,  # 当前页码
            "image":image
        }

        # 返回包含新闻列表的响应，确保传递正确的 response_data 参数
        ResponseUtils.ok(self.handler, result_dict)  # 修正了拼写错误

    @exception_catcher
    @auth_required
    def post(self):
        data = self.json_utils.parse_json(self.handler)
        tid=data.get('id')
        if not tid:
            raise BadRequestException("Missing 'id' in request body")

        if news_delete(tid):
            response_data = {
                "is_delete":"ok"
            }
            ResponseUtils.ok(self.handler, response_data)



