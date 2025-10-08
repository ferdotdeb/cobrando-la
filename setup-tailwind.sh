#!/bin/bash
# Script de setup completo de Tailwind CSS para producción
# Ejecutar desde la raíz del proyecto Django

set -e  # Detener si hay algún error

echo "🚀 Instalando Tailwind CSS para producción..."

# 1. Instalar dependencias de Node.js
echo "📦 Instalando dependencias de Node.js..."
npm install

# 2. Compilar CSS para producción
echo "🎨 Compilando Tailwind CSS (minificado)..."
npm run build:css

# 3. Instalar WhiteNoise (si no está instalado)
echo "📚 Instalando WhiteNoise..."
if command -v uv &> /dev/null; then
    uv pip install whitenoise
else
    pip install whitenoise
fi

# 4. Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos con hash..."
python manage.py collectstatic --noinput

echo ""
echo "✅ ¡Setup completado con éxito!"
echo ""
echo "📊 Verificación:"
echo "  - CSS compilado: static/build/tailwind.css"
echo "  - CSS con hash: staticfiles/build/tailwind.*.css"
echo ""
echo "🎯 Próximos pasos:"
echo "  1. Desarrollo: npm run dev:css (en una terminal) + python manage.py runserver"
echo "  2. Producción: Ejecutar este script antes de cada deploy"
echo ""
