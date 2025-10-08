# Tailwind CSS - Setup de Producción

## ✅ Configuración completada

Este proyecto está configurado para usar Tailwind CSS en producción sin CDN, con compilación local y servicio de archivos estáticos optimizados mediante WhiteNoise.

## 📁 Archivos creados/modificados

### Archivos de configuración creados:
- `package.json` - Dependencias de Node.js y scripts de build
- `tailwind.config.js` - Configuración de Tailwind CSS
- `postcss.config.js` - Configuración de PostCSS
- `assets/css/input.css` - CSS de entrada para Tailwind
- `templates/base.html` - Template base con Tailwind incluido
- `templates/tailwind-test.html` - Template de prueba

### Archivos modificados:
- `cobrando_la/settings.py` - Configuración de Django para WhiteNoise y estáticos
- `requirements.txt` - Añadido `whitenoise>=6.6.0`
- `.gitignore` - Añadidas exclusiones para Node.js y archivos generados

## 🚀 Comandos de desarrollo

### Instalación inicial (solo una vez):
```bash
# Instalar dependencias de Node.js
npm install

# Instalar WhiteNoise para Django
uv pip install whitenoise
# O si usas pip normal: pip install whitenoise
```

### Desarrollo con hot-reload del CSS:
```bash
# En una terminal, ejecutar el watcher de Tailwind
npm run dev:css

# En otra terminal, correr el servidor de Django
python manage.py runserver
```

### Build de producción:
```bash
# 1. Compilar CSS minificado
npm run build:css

# 2. Recolectar archivos estáticos con hash
python manage.py collectstatic --noinput

# 3. Ejecutar servidor (con DEBUG=False en producción)
gunicorn cobrando_la.wsgi:application
```

## 🐳 Docker / CI/CD

Si usas Docker o CI, añade estos pasos en tu pipeline:

```dockerfile
# En tu Dockerfile, antes de collectstatic:
RUN npm ci && npm run build:css
RUN python manage.py collectstatic --noinput
```

## ✅ Verificación

### 1. Verificar que el CSS está minificado:
```bash
head -n 1 static/build/tailwind.css
```
Deberías ver una línea larga y compacta sin espacios ni saltos de línea.

### 2. Verificar archivos con hash de WhiteNoise:
```bash
ls -lh staticfiles/build/
```
Deberías ver archivos como:
- `tailwind.03064092087d.css` (con hash)
- `tailwind.03064092087d.css.gz` (comprimido con gzip)

### 3. Probar en el navegador:
Accede a: http://localhost:8000/

El template base ya incluye:
```html
{% load static %}
<link rel="stylesheet" href="{% static 'build/tailwind.css' %}">
```

### 4. Template de prueba:
Para ver un ejemplo completo con clases de Tailwind, añade esta ruta en `urls.py`:

```python
from django.views.generic import TemplateView

urlpatterns = [
    # ... tus rutas existentes ...
    path('test-tailwind/', TemplateView.as_view(template_name='tailwind-test.html'), name='tailwind-test'),
]
```

Luego visita: http://localhost:8000/test-tailwind/

## 📝 Usar Tailwind en tus templates

### Opción 1: Extender el base.html
```html
{% extends 'base.html' %}

{% block title %}Mi Página{% endblock %}

{% block content %}
<div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold text-blue-600">Hola Mundo</h1>
    <button class="bg-emerald-500 hover:bg-emerald-700 text-white font-bold py-2 px-4 rounded">
        Click me
    </button>
</div>
{% endblock %}
```

### Opción 2: Incluir el CSS directamente en templates existentes
Añade al inicio de tu template HTML:
```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <!-- ... otros meta tags ... -->
    <link rel="stylesheet" href="{% static 'build/tailwind.css' %}">
</head>
```

## ⚠️ Consideraciones importantes

### Clases dinámicas
Si generas clases de Tailwind dinámicamente desde Python (ej: `f"bg-{color}-500"`), debes añadir un safelist en `tailwind.config.js`:

```javascript
module.exports = {
  content: [ /* ... */ ],
  safelist: [
    'hidden', 'block', 'flex',
    { 
      pattern: /(bg|text|border)-(red|green|blue|emerald|slate)-(100|200|500|700|900)/ 
    }
  ],
  // ...
}
```

### Producción
- **NUNCA** uses el CDN de Tailwind en producción
- **SIEMPRE** ejecuta `npm run build:css` antes de `collectstatic`
- Configura `DEBUG=False` en producción
- WhiteNoise servirá automáticamente los archivos con compresión gzip y cache headers

### Cache busting
WhiteNoise genera automáticamente hashes únicos para cada versión del CSS:
- `tailwind.css` → `tailwind.03064092087d.css`
- Esto asegura que los navegadores obtengan la versión más reciente después de cada deploy

## 🔧 Troubleshooting

### El CSS no se actualiza en el navegador
```bash
# Limpiar archivos estáticos y recompilar
rm -rf staticfiles/
npm run build:css
python manage.py collectstatic --noinput
```

### Error "Could not find backend whitenoise..."
```bash
uv pip install whitenoise
# O: pip install whitenoise
```

### Las clases de Tailwind no funcionan
1. Verifica que el template esté en las rutas de `content` en `tailwind.config.js`
2. Recompila el CSS: `npm run build:css`
3. Recarga el servidor de desarrollo

## 📦 Tamaño del build

- **CSS compilado**: ~7.7 KB (minificado)
- **CSS comprimido (gzip)**: ~2.3 KB
- Tailwind incluye solo las clases que realmente usas (tree-shaking automático)

---

**Última actualización**: 8 de octubre de 2025
