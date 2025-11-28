from fastapi import FastAPI

from app.routes.main import main_router
from app.routes.services import services_router
from app.routes.api import api_router
from app.config import settings


app = FastAPI()


settings.mount_static(app)
app.include_router(api_router)
app.include_router(services_router)
app.include_router(main_router)
