# 📋 COMANDOS LISTOS PARA COPIAR/PEGAR

## 🎯 DESARROLLO (Día a día)

### Opción 1: Dos terminales (recomendado)
```bash
# Terminal 1: Watch de Tailwind CSS (hot reload)
npm run dev:css

# Terminal 2: Servidor Django
python manage.py runserver
```

### Opción 2: Una terminal con background
```bash
# Ejecutar Tailwind en background
npm run dev:css &

# Ejecutar Django
python manage.py runserver
```

---

## 🚀 PRODUCCIÓN

### Build completo (antes de deploy)
```bash
# Compilar CSS minificado
npm run build:css

# Recolectar estáticos con hash
python manage.py collectstatic --noinput
```

### O usar el script automatizado
```bash
./setup-tailwind.sh
```

---

## 🐳 DOCKER / CI/CD

### En tu Dockerfile
```dockerfile
# Instalar Node.js
FROM python:3.11-slim
RUN apt-get update && apt-get install -y nodejs npm

# Copiar archivos
COPY package.json package-lock.json ./
COPY tailwind.config.js postcss.config.js ./
COPY assets/ ./assets/

# Instalar dependencias
RUN npm ci
RUN pip install -r requirements.txt

# Build de Tailwind
RUN npm run build:css

# Collectstatic
RUN python manage.py collectstatic --noinput

# Resto de tu Dockerfile...
```

### En GitHub Actions / GitLab CI
```yaml
# .github/workflows/deploy.yml
- name: Setup Node.js
  uses: actions/setup-node@v3
  with:
    node-version: '18'

- name: Install dependencies
  run: npm ci

- name: Build Tailwind CSS
  run: npm run build:css

- name: Collect static files
  run: python manage.py collectstatic --noinput
```

---

## 🔧 MANTENIMIENTO

### Actualizar Tailwind
```bash
npm update tailwindcss postcss autoprefixer
npm run build:css
python manage.py collectstatic --noinput
```

### Limpiar archivos generados
```bash
rm -rf staticfiles/
rm -rf static/build/
npm run build:css
python manage.py collectstatic --noinput
```

### Verificar que todo está OK
```bash
./verify-setup.sh
```

---

## 🆕 AÑADIR NUEVOS TEMPLATES

### 1. Crear template que extiende base.html
```html
{% extends 'base.html' %}

{% block title %}Mi Página{% endblock %}

{% block content %}
<div class="container mx-auto p-4">
    <h1 class="text-4xl font-bold text-blue-600">
        Hola Mundo con Tailwind
    </h1>
    
    <button class="bg-emerald-500 hover:bg-emerald-700 text-white font-bold py-2 px-4 rounded mt-4">
        Click aquí
    </button>
</div>
{% endblock %}
```

### 2. No necesitas recompilar
Las clases de Tailwind se detectan automáticamente si:
- El archivo está en las rutas de `content` en `tailwind.config.js`
- Tienes `npm run dev:css` corriendo (en desarrollo)

### 3. Para producción
```bash
npm run build:css
python manage.py collectstatic --noinput
```

---

## 🎨 PERSONALIZAR TAILWIND

### Añadir colores personalizados
```javascript
// tailwind.config.js
module.exports = {
  content: [ /* ... */ ],
  theme: {
    extend: {
      colors: {
        'brand-blue': '#1E40AF',
        'brand-green': '#10B981',
      }
    },
  },
}
```

Usar en templates:
```html
<h1 class="text-brand-blue">Mi título</h1>
```

### Añadir plugins
```bash
npm install @tailwindcss/forms @tailwindcss/typography
```

```javascript
// tailwind.config.js
module.exports = {
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

---

## ⚠️ TROUBLESHOOTING

### Los estilos no se aplican
```bash
# 1. Verificar que el template está en content de tailwind.config.js
# 2. Recompilar CSS
npm run build:css

# 3. Limpiar cache del navegador
# Ctrl+Shift+R (Chrome/Firefox)
# Cmd+Shift+R (Mac)

# 4. Verificar que el CSS se carga
# DevTools → Network → buscar "tailwind.css"
```

### Error 404 en archivos estáticos
```bash
# En desarrollo (DEBUG=True)
python manage.py runserver

# En producción, asegurar:
# - DEBUG=False
# - WhiteNoise instalado
# - collectstatic ejecutado
```

### CSS muy grande
```bash
# Verificar que solo se incluyen clases usadas
# El CSS debe ser ~7-8 KB, no MB

# Si es muy grande, revisar content en tailwind.config.js
# Asegurar que no incluyes archivos innecesarios
```

---

## 📊 VERIFICACIÓN POST-DEPLOY

### 1. Verificar archivo con hash
```bash
ls -lh staticfiles/build/
# Debe mostrar: tailwind.[HASH].css y tailwind.[HASH].css.gz
```

### 2. Verificar compresión
```bash
# Original: ~7-8 KB
du -h static/build/tailwind.css

# Comprimido: ~2-3 KB
du -h staticfiles/build/tailwind.*.css.gz
```

### 3. Verificar en producción
Abrir DevTools → Network → Buscar `tailwind.css`

Headers esperados:
```
Cache-Control: max-age=31536000, immutable
Content-Encoding: gzip
Content-Length: ~2300 bytes
```

### 4. Script de verificación
```bash
./verify-setup.sh
```

---

## 🔐 SEGURIDAD

### Variables de entorno para producción
```bash
# .env
DEBUG=False
SECRET_KEY=tu-clave-secreta-aqui
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
```

### settings.py para producción
```python
import os
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')
```

---

## 📚 RECURSOS

### Documentación creada
- `IMPLEMENTACION_COMPLETA.md` - Resumen ejecutivo
- `TAILWIND_SETUP.md` - Guía completa de setup
- `COMANDOS.md` - Este archivo
- `templates/tailwind-test.html` - Demo con ejemplos

### Scripts
- `setup-tailwind.sh` - Build completo automatizado
- `verify-setup.sh` - Verificar configuración

### Enlaces útiles
- Tailwind CSS: https://tailwindcss.com/docs
- WhiteNoise: https://whitenoise.readthedocs.io/
- Django Static Files: https://docs.djangoproject.com/en/stable/howto/static-files/

---

## ✅ CHECKLIST RÁPIDO

Antes de hacer deploy a producción:

- [ ] `npm run build:css` ejecutado
- [ ] `python manage.py collectstatic --noinput` ejecutado
- [ ] WhiteNoise instalado en requirements.txt
- [ ] STATIC_ROOT configurado en settings.py
- [ ] DEBUG=False en producción
- [ ] Archivos con hash verificados en staticfiles/
- [ ] .gitignore incluye node_modules/ y staticfiles/
- [ ] Cache del navegador probado (hash cambia en cada build)

---

**Última actualización**: 8 de octubre de 2025
