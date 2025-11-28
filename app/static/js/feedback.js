function initFeedbackForm(formId = 'feedback-form') {
    const form = document.getElementById(formId);
    if (!form) return;

    const infoBlock = form.querySelector(".form-information-block");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        form.querySelectorAll(".error").forEach(el => el.remove());

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
            if (result.detail) {
                result.detail.forEach(err => {
                    const field = err.loc.at(-1);
                    const input = form.querySelector(`[name="${field}"]`);
                    if (input) {
                        const div = document.createElement("div");
                        div.className = "error";
                        div.textContent = err.msg;
                        input.parentNode.appendChild(div);
                    }
                });
            } else {
                alert("Ошибка при отправке данных");
            }
            return;
        }

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

            // 4. Высоту формы оставляем зафиксированной (не меняем)
            // Если захочешь, можно позже сбросить height в auto
            // form.style.height = 'auto';
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    initFeedbackForm();
});
