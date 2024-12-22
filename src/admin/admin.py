from fastapi import FastAPI
from pydantic import BaseModel
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.requests import Request

from model import (
    AIAssessment,
    Answer,
    Question,
    QuestionTechnology,
    Technology,
    User,
    UserQuestion,
)


class UpdateUserPassword(BaseModel):
    password: str


class UserAdmin(ModelView, model=User):
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    column_list = [
        User.id,
        User.tg_id,
        User.tg_url,
        User.first_name,
        User.last_name,
        User.tg_username,
        User.coins,
        User.is_active,
        User.is_admin,
        User.subscription,
        User.created_at,
    ]
    column_sortable_list = [
        User.first_name,
        User.last_name,
        User.created_at,
        User.is_active,
    ]
    column_searchable_list = [
        User.first_name,
        User.last_name,
        User.tg_url,
    ]
    column_default_sort = [(User.created_at, True), (User.is_active, False)]
    column_labels = {k: v.doc for k, v in User.__mapper__.columns.items() if v.doc}
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

    async def after_model_change(
        self, data: dict, model: User, is_created: bool, request: Request
    ) -> None:
        pass
        # session_generator = db_conn.get_session()
        # session = await anext(session_generator)
        # async with session:
        #     await UserService(session=session).update(
        #         model,
        #         **UpdateUserPassword(password=data.get("password")).model_dump(),
        #     )


class TechnologyAdmin(ModelView, model=Technology):
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    column_list = [
        Technology.id,
        Technology.name,
        Technology.created_at,
    ]
    column_sortable_list = [
        Technology.name,
        Technology.created_at,
    ]
    column_searchable_list = [Technology.name]
    column_labels = {
        k: v.doc for k, v in Technology.__mapper__.columns.items() if v.doc
    }
    name = "Технология"
    name_plural = "Технологии"
    icon = "fa-solid fa-layer-group"


class QuestionAdmin(ModelView, model=Question):
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    column_list = [
        Question.id,
        Question.text,
        Question.published,
        Question.complexity,
        Question.created_at,
    ]
    column_sortable_list = [
        Question.created_at,
        Question.published,
        Question.complexity,
    ]
    column_searchable_list = [Question.text]
    column_labels = {k: v.doc for k, v in Question.__mapper__.columns.items() if v.doc}
    name = "Вопрос"
    name_plural = "Вопросы"
    icon = "fa-solid fa-question"


class QuestionTechnologyAdmin(ModelView, model=QuestionTechnology):
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    column_list = [
        QuestionTechnology.id,
        QuestionTechnology.question,
        QuestionTechnology.technology,
        QuestionTechnology.created_at,
    ]
    column_sortable_list = [
        QuestionTechnology.created_at,
    ]
    column_searchable_list = []
    column_labels = {
        k: v.doc for k, v in QuestionTechnology.__mapper__.columns.items() if v.doc
    }
    name = "Технология вопроса"
    name_plural = "Технологии вопроса"
    icon = "fa-solid fa-link"


class UserQuestionAdmin(ModelView, model=UserQuestion):
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    column_list = [
        UserQuestion.id,
        UserQuestion.user,
        UserQuestion.question,
        UserQuestion.created_at,
    ]
    column_sortable_list = [
        UserQuestion.created_at,
        UserQuestion.user,
        UserQuestion.question,
    ]
    column_searchable_list = []
    column_labels = {
        k: v.doc for k, v in UserQuestion.__mapper__.columns.items() if v.doc
    }
    name = "Вопрос пользователя"
    name_plural = "Вопросы пользователя"
    icon = "fa-solid fa-link"


class AnswerAdmin(ModelView, model=Answer):
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    column_list = [
        Answer.id,
        Answer.user,
        Answer.question,
        Answer.text,
        Answer.score,
        Answer.created_at,
    ]
    column_sortable_list = [
        Answer.score,
        Answer.created_at,
    ]
    column_searchable_list = [Answer.text]
    column_labels = {k: v.doc for k, v in Answer.__mapper__.columns.items() if v.doc}
    name = "Ответ"
    name_plural = "Ответы"
    icon = "fa-solid fa-lightbulb"


class AIAssessmentAdmin(ModelView, model=AIAssessment):
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    column_list = [
        AIAssessment.id,
        AIAssessment.created_at,
        AIAssessment.user,
        AIAssessment.question,
        AIAssessment.answer,
    ]
    column_sortable_list = [
        AIAssessment.created_at,
    ]
    column_searchable_list = [AIAssessment.text]
    column_labels = {
        k: v.doc for k, v in AIAssessment.__mapper__.columns.items() if v.doc
    }
    name = "Ответ модели"
    name_plural = "Ответы модели"
    icon = "fa-solid fa-brain"


def init_admin(
    app: FastAPI,
    engine: AsyncEngine,
    title: str,
    authentication_backend: AuthenticationBackend,
):
    admin = Admin(
        app=app,
        engine=engine,
        title=title,
        authentication_backend=authentication_backend,
    )

    admin.add_view(UserAdmin)
    admin.add_view(TechnologyAdmin)
    admin.add_view(QuestionAdmin)
    admin.add_view(QuestionTechnologyAdmin)
    admin.add_view(UserQuestionAdmin)
    admin.add_view(AnswerAdmin)
    admin.add_view(AIAssessmentAdmin)

    return admin
