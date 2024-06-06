from applications.base import APIView
from middleware.exceptions import BadRequestException
from middleware.exception_catcher import exception_catcher
from database.db import get_session
from database.models import message
from sqlmodel import select

class generate_url(APIView):
