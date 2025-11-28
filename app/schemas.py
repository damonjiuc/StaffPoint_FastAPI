from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class Feedback(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    phone: str = Field(...)
    email: EmailStr | None = None
    subject: str = Field(..., min_length=2)
    message: str = Field(..., min_length=5, max_length=2000)

    # --- Валидация телефона ---
    @field_validator("phone")
    def validate_phone(cls, v):
        digits = re.sub(r"\D", "", v)

        # Привести 8XXXXXXXXXX → 7XXXXXXXXXX
        if digits.startswith("8"):
            digits = "7" + digits[1:]

        # Должно начинаться на 7
        if not digits.startswith("7"):
            raise ValueError("Телефон должен начинаться с +7")

        if len(digits) != 11:
            raise ValueError("Телефон должен содержать 11 цифр")

        # Форматирование
        formatted = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
        return formatted
