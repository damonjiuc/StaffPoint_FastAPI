function initFeedbackForm(formId = 'feedback-form') {
    const form = document.getElementById(formId);
    if (!form) return;

    const infoBlock = form.querySelector(".form-information-block");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Удаляем старые ошибки
        const errorsBox = form.querySelector(".form-feedback-errors");
        errorsBox.innerHTML = "";

        errorsBox.style.display = "none";

        const data = Object.fromEntries(new FormData(form).entries());

        let response;
        try {
            response = await fetch("/api/feedback", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });
        } catch (err) {
            showMessage("Ошибка соединения. Попробуйте позже.");
            return;
        }

        const result = await response.json();

        if (!response.ok) {

            // Если есть detail → ошибки валидации FastAPI/Pydantic
            if (result.detail) {
                result.detail.forEach(err => {
                    // Показываем контейнер
                    errorsBox.style.display = "block";

                    const div = document.createElement("div");
                    div.className = "error";
                    div.textContent = err.msg.replace(/^Value error,\s*/i, "");
                    errorsBox.appendChild(div);
                });
            } else {
                // Непредвиденная ошибка сервера
                const div = document.createElement("div");
                div.className = "error";
                div.textContent = "Ошибка при отправке данных";
                errorsBox.appendChild(div);
            }

            return;
        }

        ym(105557919,'reachGoal','feedback_sent');
        console.log("Метрика: цель feedback_sent отправлена");

        showMessage(result.message || "Ваша заявка отправлена, мы обязательно с Вами свяжемся!");

        function showMessage(message) {
            // 1. Фиксируем текущую высоту формы
            const startHeight = form.scrollHeight;
            form.style.height = startHeight + "px";
            form.style.overflow = "hidden";
            form.style.transition = "height 0.5s ease";

            // 2. Заменяем содержимое infoBlock
            infoBlock.innerHTML = `<div class="form-success">${message}</div>`;

            // 3. Плавное появление текста через opacity
            const successDiv = infoBlock.querySelector(".form-success");
            requestAnimationFrame(() => {
                successDiv.classList.add("visible");
            });
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    initFeedbackForm();
});
