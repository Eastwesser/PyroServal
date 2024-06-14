FROM python:3.10-slim

# Установитe переменные окружения
ENV PYTHONUNBUFFERED=1

# Установитe рабочий каталог
WORKDIR /app

# Скачайте зависимости
COPY requirements.txt /app/

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте остальной код приложения
COPY . /app/

# Start the bot
CMD ["python", "-m", "app.main"]