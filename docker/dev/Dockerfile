FROM python:3.13-slim

WORKDIR /app

RUN apt update -y && apt install git -y && apt install -y nodejs npm

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py tailwind install