#!/bin/bash
# Checklist de verificación post-implementación
# Ejecutar para validar que todo está correctamente configurado

echo "🔍 VERIFICANDO IMPLEMENTACIÓN DE TAILWIND CSS..."
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función de verificación
check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1"
    fi
}

# 1. Verificar archivos de configuración
echo "📁 Verificando archivos de configuración..."
[ -f "package.json" ] && check "package.json existe" || echo -e "${RED}✗${NC} package.json NO existe"
[ -f "tailwind.config.js" ] && check "tailwind.config.js existe" || echo -e "${RED}✗${NC} tailwind.config.js NO existe"
[ -f "postcss.config.js" ] && check "postcss.config.js existe" || echo -e "${RED}✗${NC} postcss.config.js NO existe"
[ -f "assets/css/input.css" ] && check "assets/css/input.css existe" || echo -e "${RED}✗${NC} assets/css/input.css NO existe"
echo ""

# 2. Verificar node_modules
echo "📦 Verificando dependencias Node.js..."
[ -d "node_modules" ] && check "node_modules instalado" || echo -e "${RED}✗${NC} Ejecutar: npm install"
[ -d "node_modules/tailwindcss" ] && check "tailwindcss instalado" || echo -e "${RED}✗${NC} tailwindcss NO instalado"
[ -d "node_modules/postcss" ] && check "postcss instalado" || echo -e "${RED}✗${NC} postcss NO instalado"
[ -d "node_modules/autoprefixer" ] && check "autoprefixer instalado" || echo -e "${RED}✗${NC} autoprefixer NO instalado"
echo ""

# 3. Verificar CSS compilado
echo "🎨 Verificando CSS compilado..."
[ -f "static/build/tailwind.css" ] && check "CSS compilado existe" || echo -e "${RED}✗${NC} Ejecutar: npm run build:css"
if [ -f "static/build/tailwind.css" ]; then
    SIZE=$(du -h static/build/tailwind.css | cut -f1)
    echo -e "${GREEN}  →${NC} Tamaño: $SIZE"
fi
echo ""

# 4. Verificar archivos estáticos con hash
echo "🔐 Verificando archivos con hash (WhiteNoise)..."
[ -d "staticfiles" ] && check "staticfiles/ existe" || echo -e "${YELLOW}⚠${NC} Ejecutar: python manage.py collectstatic --noinput"
if [ -d "staticfiles/build" ]; then
    HASHED=$(ls staticfiles/build/tailwind.*.css 2>/dev/null | head -1)
    if [ -n "$HASHED" ]; then
        check "Archivo con hash existe"
        echo -e "${GREEN}  →${NC} $(basename $HASHED)"
    else
        echo -e "${YELLOW}⚠${NC} No se encontró archivo con hash"
    fi
fi
echo ""

# 5. Verificar compresión gzip
echo "📦 Verificando compresión gzip..."
GZIPPED=$(ls staticfiles/build/tailwind.*.css.gz 2>/dev/null | head -1)
if [ -n "$GZIPPED" ]; then
    check "Archivo gzip existe"
    SIZE=$(du -h "$GZIPPED" | cut -f1)
    echo -e "${GREEN}  →${NC} Tamaño comprimido: $SIZE"
else
    echo -e "${YELLOW}⚠${NC} No se encontró archivo gzip (ejecutar collectstatic)"
fi
echo ""

# 6. Verificar WhiteNoise instalado
echo "🔧 Verificando WhiteNoise..."
if python -c "import whitenoise" 2>/dev/null; then
    check "WhiteNoise instalado"
    VERSION=$(python -c "import whitenoise; print(whitenoise.__version__)" 2>/dev/null)
    echo -e "${GREEN}  →${NC} Versión: $VERSION"
else
    echo -e "${RED}✗${NC} WhiteNoise NO instalado (ejecutar: uv pip install whitenoise)"
fi
echo ""

# 7. Verificar configuración en settings.py
echo "⚙️  Verificando settings.py..."
if grep -q "whitenoise.middleware.WhiteNoiseMiddleware" cobrando_la/settings.py; then
    check "WhiteNoise middleware configurado"
else
    echo -e "${RED}✗${NC} WhiteNoise middleware NO configurado"
fi

if grep -q "CompressedManifestStaticFilesStorage" cobrando_la/settings.py; then
    check "Storage configurado correctamente"
else
    echo -e "${RED}✗${NC} Storage NO configurado"
fi

if grep -q "STATIC_ROOT" cobrando_la/settings.py; then
    check "STATIC_ROOT configurado"
else
    echo -e "${RED}✗${NC} STATIC_ROOT NO configurado"
fi
echo ""

# 8. Verificar templates
echo "📄 Verificando templates..."
[ -f "templates/base.html" ] && check "templates/base.html existe" || echo -e "${YELLOW}⚠${NC} templates/base.html NO existe"
[ -f "templates/tailwind-test.html" ] && check "templates/tailwind-test.html existe" || echo -e "${YELLOW}⚠${NC} templates/tailwind-test.html NO existe"
echo ""

# 9. Verificar .gitignore
echo "🚫 Verificando .gitignore..."
if grep -q "node_modules/" .gitignore; then
    check "node_modules/ en .gitignore"
else
    echo -e "${YELLOW}⚠${NC} node_modules/ NO está en .gitignore"
fi

if grep -q "staticfiles/" .gitignore; then
    check "staticfiles/ en .gitignore"
else
    echo -e "${YELLOW}⚠${NC} staticfiles/ NO está en .gitignore"
fi

if grep -q "static/build/" .gitignore; then
    check "static/build/ en .gitignore"
else
    echo -e "${YELLOW}⚠${NC} static/build/ NO está en .gitignore"
fi
echo ""

# Resumen final
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 RESUMEN"
echo ""

# Contar verificaciones exitosas
if [ -f "static/build/tailwind.css" ] && [ -d "node_modules" ] && [ -f "package.json" ]; then
    echo -e "${GREEN}✅ CONFIGURACIÓN BÁSICA: OK${NC}"
else
    echo -e "${RED}❌ CONFIGURACIÓN BÁSICA: INCOMPLETA${NC}"
fi

if [ -d "staticfiles/build" ] && [ -n "$HASHED" ]; then
    echo -e "${GREEN}✅ BUILD DE PRODUCCIÓN: OK${NC}"
else
    echo -e "${YELLOW}⚠️  BUILD DE PRODUCCIÓN: PENDIENTE${NC}"
    echo "   Ejecutar: npm run build:css && python manage.py collectstatic --noinput"
fi

echo ""
echo "🚀 COMANDOS ÚTILES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Desarrollo:  npm run dev:css"
echo "  Build:       npm run build:css"
echo "  Collectstatic: python manage.py collectstatic --noinput"
echo "  Build completo: ./setup-tailwind.sh"
echo ""
