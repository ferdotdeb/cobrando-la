# 🐳 DOCKER - Tailwind CSS + Django

## 📦 Build de la imagen

### Build simple
```bash
docker build -t cobrando-la:latest .
```

### Build con argumentos
```bash
docker build \
  --build-arg SECRET_KEY=tu-secret-key \
  -t cobrando-la:latest .
```

---

## 🚀 Ejecutar contenedor

### Desarrollo
```bash
docker run -p 8000:8000 \
  -e DEBUG=True \
  -v $(pwd):/app \
  cobrando-la:latest \
  python manage.py runserver 0.0.0.0:8000
```

### Producción
```bash
docker run -p 8000:8000 \
  -e DEBUG=False \
  -e SECRET_KEY=tu-secret-key-seguro \
  -e ALLOWED_HOSTS=tudominio.com,www.tudominio.com \
  cobrando-la:latest
```

---

## 🐳 Docker Compose

### Desarrollo
```bash
# Levantar servicio de desarrollo
docker-compose up web

# Con hot reload de Tailwind (modificar docker-compose.yml primero)
docker-compose up web
```

### Producción
```bash
# Levantar servicio de producción
docker-compose up web-prod

# En background
docker-compose up -d web-prod
```

### Rebuild después de cambios
```bash
docker-compose build
docker-compose up -d
```

---

## 📋 Dockerfile explicado

```dockerfile
# Base de Python 3.13
FROM python:3.13-slim

# Directorio de trabajo
WORKDIR /app

# Instalar Node.js para Tailwind CSS
RUN apt-get update && apt-get install -y nodejs npm

# Copiar archivos de dependencias primero (cache de Docker)
COPY requirements.txt package.json ./

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt
RUN npm ci --only=production

# Copiar configuración de Tailwind
COPY tailwind.config.js postcss.config.js ./
COPY assets ./assets

# Copiar el resto de la aplicación
COPY . .

# BUILD DE TAILWIND CSS (minificado)
RUN npm run build:css

# COLLECTSTATIC con WhiteNoise (hash manifest)
RUN python manage.py collectstatic --noinput

# Usar Gunicorn para producción
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cobrando_la.wsgi:application"]
```

---

## 🎯 Flujo de build

El Dockerfile ejecuta estos pasos automáticamente:

1. ✅ Instala Node.js y npm
2. ✅ Instala dependencias Python (requirements.txt)
3. ✅ Instala dependencias Node (package.json)
4. ✅ Compila Tailwind CSS minificado (npm run build:css)
5. ✅ Recolecta estáticos con hash (collectstatic)
6. ✅ Levanta Gunicorn en producción

**Resultado:** Imagen lista para producción con Tailwind compilado y optimizado.

---

## ⚡ Optimizaciones aplicadas

### Cache de capas de Docker
```dockerfile
# ✅ CORRECTO: Copiar dependencias primero
COPY requirements.txt package.json ./
RUN pip install -r requirements.txt
RUN npm ci
COPY . .  # Copiar código después

# ❌ INCORRECTO: Copiar todo junto
COPY . .
RUN pip install -r requirements.txt
```

### .dockerignore
Excluye archivos innecesarios para reducir tamaño:
- `node_modules/` (se instala en el build)
- `staticfiles/` (se genera en el build)
- `.venv/`, `__pycache__/`
- Archivos de desarrollo

### Multi-stage build (opcional avanzado)
Para reducir aún más el tamaño de la imagen:

```dockerfile
# Stage 1: Build
FROM python:3.13-slim as builder
WORKDIR /app
RUN apt-get update && apt-get install -y nodejs npm
COPY requirements.txt package.json ./
RUN pip install --no-cache-dir -r requirements.txt
RUN npm ci --only=production
COPY . .
RUN npm run build:css
RUN python manage.py collectstatic --noinput

# Stage 2: Runtime
FROM python:3.13-slim
WORKDIR /app
RUN pip install gunicorn whitenoise
COPY --from=builder /app/staticfiles ./staticfiles
COPY --from=builder /app .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cobrando_la.wsgi:application"]
```

---

## 🔧 Variables de entorno

### Desarrollo
```bash
DEBUG=True
PYTHONUNBUFFERED=1
```

### Producción
```bash
DEBUG=False
SECRET_KEY=tu-secret-key-seguro-de-50-caracteres
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
DATABASE_URL=postgres://user:pass@host:5432/db  # Si usas PostgreSQL
```

---

## 📊 Verificar el build

### Ver archivos estáticos generados
```bash
docker run --rm cobrando-la:latest ls -lh /app/staticfiles/build/
```

Deberías ver:
```
tailwind.03064092087d.css
tailwind.03064092087d.css.gz
```

### Ver tamaño de la imagen
```bash
docker images cobrando-la:latest
```

### Inspeccionar capas
```bash
docker history cobrando-la:latest
```

---

## 🚀 Deploy en producción

### Docker directo
```bash
# Build
docker build -t cobrando-la:v1.0.0 .

# Tag para registry
docker tag cobrando-la:v1.0.0 registry.tudominio.com/cobrando-la:v1.0.0

# Push
docker push registry.tudominio.com/cobrando-la:v1.0.0

# Deploy
docker run -d \
  -p 80:8000 \
  -e DEBUG=False \
  -e SECRET_KEY=$SECRET_KEY \
  -e ALLOWED_HOSTS=tudominio.com \
  --name cobrando-la \
  --restart unless-stopped \
  registry.tudominio.com/cobrando-la:v1.0.0
```

### Docker Swarm / Kubernetes
Ver documentación específica de tu orquestador.

---

## 🔍 Troubleshooting

### CSS no se compila
```bash
# Verificar que Node.js está instalado en el build
docker build --progress=plain -t cobrando-la:latest .

# Revisar logs del build
docker logs <container-id>
```

### Archivos estáticos no se sirven
```bash
# Verificar que collectstatic se ejecutó
docker run --rm cobrando-la:latest ls -lh /app/staticfiles/

# Verificar settings.py
docker run --rm cobrando-la:latest python manage.py check --deploy
```

### Imagen muy grande
```bash
# Ver tamaño actual
docker images cobrando-la:latest

# Optimizar:
# 1. Usar python:3.13-slim-alpine (más pequeña)
# 2. Implementar multi-stage build
# 3. Limpiar cache de apt después de instalar
# 4. Usar npm ci en lugar de npm install
```

---

## 📚 Comandos útiles

```bash
# Build sin cache
docker build --no-cache -t cobrando-la:latest .

# Ver logs
docker logs -f <container-id>

# Ejecutar comando en contenedor
docker exec -it <container-id> python manage.py shell

# Acceder al shell del contenedor
docker exec -it <container-id> bash

# Eliminar contenedores e imágenes
docker-compose down
docker rmi cobrando-la:latest

# Limpiar todo Docker
docker system prune -a
```

---

## ✅ Checklist pre-deploy

- [ ] ✅ `DEBUG=False` en producción
- [ ] ✅ `SECRET_KEY` configurado (no usar el default)
- [ ] ✅ `ALLOWED_HOSTS` configurado correctamente
- [ ] ✅ Build de Docker exitoso sin errores
- [ ] ✅ CSS compilado verificado en /app/staticfiles/
- [ ] ✅ Gunicorn configurado (workers, timeout)
- [ ] ✅ Variables de entorno en archivo .env o secrets
- [ ] ✅ Healthcheck configurado (opcional)
- [ ] ✅ Logs configurados para producción
- [ ] ✅ Reverse proxy (Nginx/Traefik) configurado

---

**Última actualización:** 8 de octubre de 2025  
**Estado:** ✅ Dockerfile optimizado para producción con Tailwind CSS
