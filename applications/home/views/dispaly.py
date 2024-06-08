from applications.base import APIView
from middleware.exceptions import BadRequestException
from middleware.exception_catcher import exception_catcher
from database.db import get_session
from database.models.news import News
from middleware.token_authentication import verify_token
import datetime


class HomeAPIView(APIView):
    @verify_token
    @exception_catcher
    def get(self, page=1):
        page_size = 10  # 每页显示的新闻条目数

        with get_session() as session:
            # 查询新闻条目，并应用分页
            results = session.query(News).order_by(News.timestamp.desc()) \
                .offset((page - 1) * page_size).limit(page_size).all()
        if not results:

            return BadRequestException('No news found')

        news_list = []
        for result in results:
            # 提取新闻的必要字段
            news_dict = {
                "title": result.title,
                "url": result.url,
                "department": result.department,
                "time": datetime.datetime.fromtimestamp(result.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                "clik_num":result.clik_num
            }
            news_list.append(news_dict)

        result_dict = {
            "news": news_list,
            "len": len(news_list),  # 当前页新闻的条目数
            "page": page,  # 当前页码
        }

        # 返回包含新闻列表的响应
        self.response_utils.ok(self.handler, result_dict)
