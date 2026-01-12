from pydantic import BaseModel, Field, field_validator, model_validator
import re


EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@"      # local part
    r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"   # domain
)

class Feedback(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None
    subject: str = Field(..., min_length=2)
    message: str | None = None

    # --- Валидация email ---
    @field_validator("email")
    def validate_email(cls, v):
        if not v or not v.strip():
            return None  # email необязательный

        email = v.strip()

        if not EMAIL_REGEX.match(email):
            raise ValueError("Некорректный email")

        return email

    # --- Валидация телефона ---
    @field_validator('phone')
    def validate_phone(cls, v):
        if not v or not v.strip():
            return None

        digits = re.sub(r'\D', '', v)

        # Привести 8XXXXXXXXXX → 7XXXXXXXXXX
        if digits.startswith('8'):
            digits = '7' + digits[1:]

        # Должно начинаться на 7
        if not digits.startswith('7'):
            raise ValueError('Телефон должен начинаться с +7')

        if len(digits) != 11:
            raise ValueError('Телефон должен содержать 11 цифр')

        # Форматирование
        formatted = f'+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}'
        return formatted


    # Обязательное наличие контакта
    @model_validator(mode='after')
    def check_contact(self):
        if not self.email and not self.phone:
            raise ValueError('Укажите телефон или email')
        return self
