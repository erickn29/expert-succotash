from fastapi import FastAPI

from admin.admin import init_admin
from admin.auth import authentication_backend
from core.config import config
from core.database import db_conn


app = FastAPI(
    title="Python Russia",
    version="0.0.1",
    docs_url="/swagger/" if config.app.debug else None,
    redoc_url="/redoc/" if config.app.debug else None,
    debug=config.app.debug,
)


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=config.cors.ALLOWED_HOSTS,
#     allow_credentials=config.cors.ALLOWED_CREDENTIALS,
#     # allow_origin_regex=config.CORS_ALLOWED_HOSTS_REGEX,
#     allow_methods=config.cors.ALLOWED_METHODS,
#     allow_headers=config.cors.ALLOWED_HEADERS,
# )


# app.include_router(routers)

init_admin(
    title="SobesAdmin",
    app=app,
    engine=db_conn.engine,
    authentication_backend=authentication_backend,
)
