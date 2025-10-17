FROM python:3.13-slim 

WORKDIR /app

RUN apt update && apt install -y --no-install-recommends nodejs npm && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py tailwind install
RUN python manage.py tailwind build

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000