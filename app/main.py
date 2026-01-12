from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException
from fastapi.responses import HTMLResponse

from app.routes.main import main_router
from app.routes.redirects import redirects_router
from app.routes.services import services_router
from app.routes.api import api_router
from app.config import settings
from app.services.regions import url_for_service, regions

app = FastAPI()


settings.mount_static(app)
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