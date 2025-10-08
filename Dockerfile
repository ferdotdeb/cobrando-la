FROM python:3.13-slim

WORKDIR /app

# Instalar Node.js y npm para Tailwind CSS
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .
COPY package.json .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar dependencias de Node.js
RUN npm ci --only=production

# Copiar configuración de Tailwind
COPY tailwind.config.js .
COPY postcss.config.js .
COPY assets ./assets

# Copiar el resto de la aplicación
COPY . .

# Build de Tailwind CSS (minificado para producción)
RUN npm run build:css

# Recolectar archivos estáticos con WhiteNoise
RUN python manage.py collectstatic --noinput

# Exponer puerto
EXPOSE 8000

# Comando para producción (usar gunicorn en lugar de runserver)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cobrando_la.wsgi:application"]
