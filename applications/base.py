from middleware.json_utils import JSONUtils
from middleware.exception_catcher import exception_catcher
from middleware.responses import ResponseUtils
from middleware.exceptions import APIException


class APIView:
    def __init__(self, handler, query_params=None, headers=None, post_data=None):
        self.handler = handler
        self.query_params = query_params
        self.headers = headers
        self.post_data = post_data
        self.json_utils = JSONUtils
        self.response_utils = ResponseUtils

    @exception_catcher
    def handle_request(self):
        method = self.handler.command.lower()
        if hasattr(self, method):
            return getattr(self, method)()
        else:
            raise APIException(405, 'Method not allowed')
