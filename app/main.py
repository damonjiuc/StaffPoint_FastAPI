from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware

from app.routes.main import main_router
from app.routes.redirects import redirects_router
from app.routes.services import services_router
from app.routes.api import api_router
from app.config import settings
from app.services.admin import NewsAdmin, TagAdmin, NewsSectionAdmin, AdminAuth
from app.services.regions import url_for_service, regions
from app.database.engine import create_db, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    await create_db()
    yield
    # SHUTDOWN (ничего не делаем)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key="SuperSecretKey",  # тот же ключ
)

settings.mount_static(app)

admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=AdminAuth(secret_key="SuperSecretKey"),
    templates_dir="app/templates",
)

admin.add_view(NewsAdmin)
admin.add_view(NewsSectionAdmin)
admin.add_view(TagAdmin)


app.include_router(api_router)
app.include_router(redirects_router)
app.include_router(services_router)
app.include_router(main_router)


templates = settings.configure_templates()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            '404.html',
            {
                'request': request,
                'path': request.url.path,
                'region': None,
                'regions': regions,
                'url_for_service' : url_for_service
            },
            status_code=404,
        )

    return HTMLResponse(
        content=str(exc.detail),
        status_code=exc.status_code
    )