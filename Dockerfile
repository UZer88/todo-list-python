FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Переменная окружения для Python
ENV PYTHONPATH=/app

# Открываем порт
EXPOSE 8000

# Запускаем веб-версию
CMD ["uvicorn", "web_app:app", "--host", "0.0.0.0", "--port", "8000"]
