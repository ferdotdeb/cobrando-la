# Stage 1: Compile tailwind

FROM python:3.13-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install django-tailwind

COPY . .
RUN python manage.py tailwind install
RUN python manage.py tailwind build --production

# Stage 2: Production image

FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project and static files

COPY --from=builder /app /app
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "cobrando_la.wsgi:application", "--bind", "0.0.0.0:8000"]