from applications.base import APIView
from middleware.exceptions import BadRequestException
from middleware.exception_catcher import exception_catcher
from applications.User.utils.hash_password import hash_password
from applications.User.utils.generate_unique_uid import generate_id
from database.models.user import User
from database.db import get_session


class UserSignupView(APIView):
    @exception_catcher
    def post(self):
        data = self.json_utils.parse_json(self.handler)

        username = data.get('username')
        password = data.get('password')
        phone = data.get('phone')

        if not all([username, password, phone]):
            raise BadRequestException("Missing required fields")

        hashed_password = hash_password(password)
        uid = generate_id()
        user = User(id=uid, username=username, password=hashed_password, phone=phone)

        with get_session() as session:
            session.add(user)
            session.commit()

        response_data = {'uid': uid}
        self.response_utils.ok(self.handler, response_data)
