from applications.base import APIView
from middleware.exceptions import BadRequestException, NotFoundException
from middleware.exception_catcher import exception_catcher
from applications.User.utils.hash_password import verify_password
from middleware.token_generator import generate_token
from database.db import get_session
from database.models.user import User
from sqlmodel import select


class UserLoginView(APIView):
    @exception_catcher
    def post(self):
        data = self.json_utils.parse_json(self.handler)

        phone = data.get('phone')
        password = data.get('password')

        if not all([phone, password]):
            raise BadRequestException('Missing required fields')

        with get_session() as session:
            statement = select(User).where(User.phone == phone)
            results = session.exec(statement)
            user = results.one_or_none()
            if user and verify_password(user.password, password):
                token = generate_token(user)
                response_data = {'token': token}
                self.response_utils.ok(self.handler, response_data)
            else:
                raise NotFoundException('Invalid phone or password')
