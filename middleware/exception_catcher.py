from middleware.exceptions import APIException, InternalErrorException
from middleware.responses import ResponseUtils


def exception_catcher(func):
    def wrapper(handler, *args, **kwargs):
        try:
            return func(handler, *args, **kwargs)
        except APIException as e:
            ResponseUtils.send_error(handler, e)
        except Exception as e:
            ResponseUtils.send_error(handler, InternalErrorException(str(e)))

    return wrapper
