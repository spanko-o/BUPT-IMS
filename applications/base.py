from middleware.json_utils import JSONUtils
from middleware.exception_catcher import exception_catcher
from middleware.responses import ResponseUtils
from middleware.exceptions import APIException


class APIView:
    def __init__(self, handler):
        self.handler = handler
        self.json_utils = JSONUtils
        self.response_utils = ResponseUtils

    @exception_catcher
    def handle_request(self):
        method = self.handler.command.lower()
        if hasattr(self, method):
            return getattr(self, method)()
        else:
            raise APIException(405, 'Method not allowed')
