from sqlalchemy.ext.asyncio import AsyncSession

from model.question import Question
from repository.base import BaseRepository


class QuestionRepository(BaseRepository):
    model = Question

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
