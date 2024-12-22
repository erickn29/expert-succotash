# from apps.v1.auth.utils.auth import JWTAuthenticationBackend as auth
#
# # from model.user import UserRole
# from apps.v1.user.service import UserService
# from core.database import db_conn

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from core.cache import cache
from core.config import config


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str) -> None:
        super().__init__(secret_key)

    async def login(self, request: Request) -> bool:
        return False

    async def logout(self, request: Request) -> bool:
        if not request.session.get("token"):
            return False

        del request.session["token"]  # TODO удаляются все куки решить!
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if token and await cache.get(token):
            return True
        token = request.query_params.get("token")
        if token and await cache.get(token):
            request.session["token"] = token
            return True
        return False


authentication_backend = AdminAuth(secret_key=config.app.secret_key)
