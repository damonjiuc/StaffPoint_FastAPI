from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import JSONResponse
import shutil
from uuid import uuid4

from app.config import settings
from app.schemas import Feedback
from app.services.mailer import send_email

api_router = APIRouter(
    tags=['API'],
    prefix='/api'
)

@api_router.post("/feedback")
async def send_feedback(form: Feedback):

    html = f"""
    <h2>Новое сообщение с сайта</h2>
    <p><b>Имя:</b> {form.name}</p>
    <p><b>Email:</b> {form.email}</p>
    <p><b>Телефон:</b> {form.phone}</p>
    <p><b>Услуга:</b> {form.subject}</p>
    <p><b>Сообщение:</b><br>{form.message}</p>
    """

    await send_email(
        to_email="f.kerov@staffpoint.ru",
        subject="Новое обращение с сайта",
        message_html=html,
        message_text=form.message
    )

    return {"success": True}


@api_router.post("/upload-image/")
async def upload_image(request: Request, file: UploadFile = File(...)):
    # создаём уникальное имя
    ext = file.filename.split(".")[-1]
    filename = f"{uuid4().hex}.{ext}"
    file_path = settings.UPLOAD_DIR / filename

    # сохраняем файл
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # возвращаем URL, который TinyMCE сможет вставить
    url = f"/static/uploads/{filename}"
    return JSONResponse({"location": str(url)})