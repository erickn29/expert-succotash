from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base import Base


class Technology(Base):
    __tablename__ = "technology"

    name: Mapped[str] = mapped_column(String, nullable=False, doc="Название технологии")

    question_technologies = relationship(
        "QuestionTechnology", back_populates="technology"
    )

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
