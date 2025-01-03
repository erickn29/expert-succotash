from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base import Base


class QuestionTechnology(Base):
    __tablename__ = "question_technology"
    __table_args__ = (UniqueConstraint("question_id", "technology_id"),)
    verbose_name: str = "Технология вопроса"

    question_id: Mapped[int] = mapped_column(
        ForeignKey("question.id"), nullable=False, doc="Вопрос", name="question_id"
    )
    technology_id: Mapped[int] = mapped_column(
        ForeignKey("technology.id"),
        nullable=False,
        doc="Технология",
        name="technology_id",
    )

    question = relationship(
        "Question",
        back_populates="question_technologies",
        uselist=False,
        lazy="joined"
    )
    technology = relationship(
        "Technology",
        back_populates="question_technologies",
        uselist=False,
        lazy="joined"
    )

    def __repr__(self):
        return f"{str(self.question)[:20]} | {str(self.technology)[:10]}"
