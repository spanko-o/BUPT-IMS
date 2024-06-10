from applications.base import APIView
from middleware.exceptions import BadRequestException
from middleware.exception_catcher import exception_catcher
from database.db import get_session
from database.models.news import News
from middleware.token_authentication import auth_required
from middleware.responses import ResponseUtils
from sqlmodel import select

class DetailsView(APIView):

    def __init__(self, handler):
        super().__init__(handler)

    @exception_catcher
    @auth_required
    def get(self):
        id = self.query_params.get('id', [''])[0]

        if id is None:
            raise BadRequestException('The web is not found')

        else:
            with get_session() as session:
                statement=select(News).filter(News.id == id)
                result = session.exec(statement).first()

            if result is None:
                raise BadRequestException('The web is not found')

            result_dict = {
                "title": result.title,
                "department": result.department,
                "time": result.time.strftime('%Y-%m-%d %H:%M:%S'),
                "content": result.content,
                "click_num": result.click_num
            }




        # 返回包含新闻列表的响应，确保传递正确的 response_data 参数
        ResponseUtils.ok(self.handler, result_dict)  # 修正了拼写错误








