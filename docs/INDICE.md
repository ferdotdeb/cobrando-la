# 🗂️ ÍNDICE DE DOCUMENTACIÓN - Tailwind CSS

## 📖 Guías de lectura recomendadas

### 🚀 Para empezar AHORA (5 minutos)
→ **README_TAILWIND.md**
- Quick start
- Comandos básicos
- Verificación rápida

### 📋 Para entender QUÉ se hizo (10 minutos)
→ **IMPLEMENTACION_COMPLETA.md**
- Resumen ejecutivo
- Archivos creados y modificados
- Verificación del build
- Métricas

### 💻 Para comandos copy/paste (referencia)
→ **COMANDOS.md**
- Desarrollo
- Producción
- Docker/CI/CD
- Troubleshooting
- Personalización

### 📚 Para configuración detallada (cuando lo necesites)
→ **TAILWIND_SETUP.md**
- Setup completo paso a paso
- Configuración avanzada
- Troubleshooting detallado
- Consideraciones de producción

---

## 🛠️ Scripts disponibles

### `setup-tailwind.sh`
Build completo automatizado:
- Instala dependencias npm
- Compila CSS minificado
- Instala WhiteNoise
- Ejecuta collectstatic

**Uso:**
```bash
./setup-tailwind.sh
```

### `verify-setup.sh`
Verificación de la configuración:
- Verifica archivos de configuración
- Verifica dependencias instaladas
- Verifica CSS compilado
- Verifica archivos con hash
- Verifica compresión gzip

**Uso:**
```bash
./verify-setup.sh
```

---

## 📁 Estructura de archivos

```
cobrando-la/
├── 📄 package.json                   # npm config
├── 📄 tailwind.config.js             # Tailwind config
├── 📄 postcss.config.js              # PostCSS config
├── 📄 requirements.txt               # Python deps (con whitenoise)
│
├── 📁 assets/
│   └── 📁 css/
│       └── input.css                 # CSS de entrada
│
├── 📁 static/
│   └── 📁 build/
│       └── tailwind.css              # CSS compilado (7.7 KB)
│
├── 📁 staticfiles/                   # Generado por collectstatic
│   └── 📁 build/
│       ├── tailwind.[hash].css       # CSS con hash
│       └── tailwind.[hash].css.gz    # CSS comprimido (2.3 KB)
│
├── 📁 templates/
│   ├── base.html                     # Template base
│   └── tailwind-test.html            # Demo
│
├── 📁 cobrando_la/
│   └── settings.py                   # Django settings (modificado)
│
├── 🔧 setup-tailwind.sh              # Script de build
├── 🔧 verify-setup.sh                # Script de verificación
│
└── 📚 Documentación/
    ├── README_TAILWIND.md            # ⭐ EMPEZAR AQUÍ
    ├── IMPLEMENTACION_COMPLETA.md    # Resumen ejecutivo
    ├── COMANDOS.md                   # Comandos listos
    ├── TAILWIND_SETUP.md             # Guía completa
    └── INDICE.md                     # Este archivo
```

---

## ⚡ Quick Reference

### Desarrollo
```bash
npm run dev:css                    # Watch CSS (hot reload)
python manage.py runserver         # Django server
```

### Producción
```bash
npm run build:css                  # Build minificado
python manage.py collectstatic --noinput   # Collectstatic
# O:
./setup-tailwind.sh               # Todo en uno
```

### Verificación
```bash
./verify-setup.sh                 # Verificar configuración
```

---

## 🎯 Rutas de aprendizaje

### Soy nuevo en Tailwind
1. Leer: `README_TAILWIND.md` (sección "Usar en templates")
2. Ver: `templates/tailwind-test.html` (ejemplos)
3. Probar: Añadir clases en tus templates
4. Consultar: https://tailwindcss.com/docs

### Quiero deployear a producción
1. Leer: `COMANDOS.md` (sección "PRODUCCIÓN")
2. Ejecutar: `./setup-tailwind.sh`
3. Verificar: `./verify-setup.sh`
4. Leer: `IMPLEMENTACION_COMPLETA.md` (sección "Deploy en producción")

### Tengo problemas
1. Ejecutar: `./verify-setup.sh`
2. Leer: `COMANDOS.md` (sección "TROUBLESHOOTING")
3. Leer: `TAILWIND_SETUP.md` (sección "Troubleshooting")

### Quiero personalizar Tailwind
1. Leer: `COMANDOS.md` (sección "PERSONALIZAR TAILWIND")
2. Editar: `tailwind.config.js`
3. Recompilar: `npm run build:css`

---

## 📊 Checklist de verificación

Antes de hacer deploy a producción:

- [ ] ✅ `npm run build:css` ejecutado
- [ ] ✅ `python manage.py collectstatic --noinput` ejecutado
- [ ] ✅ WhiteNoise instalado en requirements.txt
- [ ] ✅ STATIC_ROOT configurado en settings.py
- [ ] ✅ DEBUG=False en producción
- [ ] ✅ Archivos con hash verificados en staticfiles/
- [ ] ✅ .gitignore incluye node_modules/ y staticfiles/
- [ ] ✅ Cache del navegador probado

---

## 🆘 Ayuda rápida

**CSS no se actualiza:**
```bash
npm run build:css
python manage.py collectstatic --noinput
# Ctrl+Shift+R en el navegador
```

**Error en collectstatic:**
```bash
uv pip install whitenoise
```

**Clases no funcionan:**
```bash
# Verificar que el template está en tailwind.config.js
npm run build:css
```

**Verificar todo:**
```bash
./verify-setup.sh
```

---

## 📞 Contacto / Soporte

Para más información, consultar:
- Documentación de Tailwind: https://tailwindcss.com/docs
- Documentación de WhiteNoise: https://whitenoise.readthedocs.io/
- Django Static Files: https://docs.djangoproject.com/en/stable/howto/static-files/

---

**Última actualización:** 8 de octubre de 2025  
**Versión:** 1.0.0  
**Estado:** ✅ Production-ready
