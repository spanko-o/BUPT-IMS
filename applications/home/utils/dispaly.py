from applications.base import APIView
from middleware.exceptions import BadRequestException
from middleware.exception_catcher import exception_catcher
from database.db import get_session
from database.models.news import News
from middleware.token_authentication import verify_token
import datetime


class NewsGetAPIView(APIView):
    @verify_token
    @exception_catcher
    def get(self, page=1):
        page_size = 10
        with get_session() as session:
            results = session.query(News).offset((page - 1) * page_size).limit(page_size).all()
        news_list = []
        if results is None:
            return BadRequestException('No news found')
        for result in results:
            title = result.title
            url = result.url
            department = result.department
            time = datetime.datetime.fromtimestamp(result.timestamp)
            news_dict = {
                "title": title,
                "url": url,
                "department": department,
                "time": time
            }
            news_list.append(news_dict)
        result_dict = {
            "news": news_list,
            "len": len(news_list)
        }
        self.response_utils.ok(self.handler, result_dict)
