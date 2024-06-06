from applications.base import APIView
from middleware.exceptions import BadRequestException
from middleware.exceptions import BadRequestException
from middleware.exception_catcher import exception_catcher
from applications.User.utils.hash_password import hash_password
from database.db import get_session
from database.models.user import User
from sqlmodel import select
class UserLoginView(APIView):
    @exception_catcher
    def post(self):
        data = self.json_utils.parse_request(self.handler)
        id_to_find=data['id']
        password=data['password']
        if not all([id,password]):
            raise BadRequestException('Missing username or password')
        hash_word=hash_password(password)
        with get_session() as session:
            statement = select(User).where(User.id == id_to_find)
        result = session.exec(statement).first()
        if result.password == hash_word:
            self.response_utils.ok()
        else:

            self.response_utils.send_error()
