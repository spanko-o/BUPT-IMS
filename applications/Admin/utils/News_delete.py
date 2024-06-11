from database.db import get_session
from sqlmodel import delete
from database.models.news import News
from middleware.exceptions import BadRequestException, InternalErrorException

def news_delete(tid):
    if tid is None:
        raise BadRequestException('The tid is required')
    with get_session() as session:
        statements=delete(News).filter(News.id == tid)
        session.commit(statements)


