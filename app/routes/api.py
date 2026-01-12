from fastapi import APIRouter, HTTPException
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
        to_email="damonjiuc@gmail.com",
        subject="Новое обращение с сайта",
        message_html=html,
        message_text=form.message
    )

    return {"success": True}