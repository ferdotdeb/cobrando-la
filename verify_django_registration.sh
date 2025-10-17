#!/bin/bash

# Script para verificar la instalación de django-registration

echo "=========================================="
echo "Verificando instalación de django-registration"
echo "=========================================="
echo ""

# Verificar que django-registration está instalado
echo "1. Verificando instalación de paquete..."
python -c "import registration; print('✓ django-registration-redux instalado correctamente')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "✗ django-registration-redux NO está instalado"
    echo "  Ejecuta: pip install django-registration-redux"
    exit 1
fi
echo ""

# Verificar configuración en settings
echo "2. Verificando configuración en settings.py..."
if grep -q "'registration'" cobrando_la/settings.py; then
    echo "✓ 'registration' está en INSTALLED_APPS"
else
    echo "✗ 'registration' NO está en INSTALLED_APPS"
    exit 1
fi

if grep -q "REGISTRATION_AUTO_LOGIN" cobrando_la/settings.py; then
    echo "✓ Configuración de REGISTRATION_AUTO_LOGIN encontrada"
else
    echo "✗ Configuración de REGISTRATION_AUTO_LOGIN NO encontrada"
    exit 1
fi

if grep -q "EMAIL_BACKEND" cobrando_la/settings.py; then
    echo "✓ Configuración de EMAIL_BACKEND encontrada"
else
    echo "✗ Configuración de EMAIL_BACKEND NO encontrada"
    exit 1
fi
echo ""

# Verificar URLs
echo "3. Verificando configuración de URLs..."
if grep -q "RegistrationView" accounts/urls.py; then
    echo "✓ RegistrationView configurado en URLs"
else
    echo "✗ RegistrationView NO configurado en URLs"
    exit 1
fi
echo ""

# Verificar templates
echo "4. Verificando templates..."
templates=(
    "accounts/templates/registration/login.html"
    "accounts/templates/registration/password_reset.html"
    "accounts/templates/registration/password_reset_done.html"
    "accounts/templates/registration/password_reset_confirm.html"
    "accounts/templates/registration/password_reset_complete.html"
    "accounts/templates/registration/password_reset_email.html"
    "accounts/templates/registration/password_reset_subject.txt"
    "accounts/templates/accounts/signup.html"
)

for template in "${templates[@]}"; do
    if [ -f "$template" ]; then
        echo "✓ $template"
    else
        echo "✗ $template NO encontrado"
        exit 1
    fi
done
echo ""

# Verificar formularios
echo "5. Verificando formularios..."
if grep -q "class UserCreationForm(RegistrationForm)" accounts/forms.py; then
    echo "✓ UserCreationForm extiende de RegistrationForm"
else
    echo "✗ UserCreationForm NO extiende de RegistrationForm"
    exit 1
fi

if grep -q "class CustomPasswordResetForm" accounts/forms.py; then
    echo "✓ CustomPasswordResetForm definido"
else
    echo "✗ CustomPasswordResetForm NO definido"
    exit 1
fi
echo ""

echo "=========================================="
echo "✓ ¡Todas las verificaciones pasaron!"
echo "=========================================="
echo ""
echo "Próximos pasos:"
echo "1. Ejecuta: python manage.py migrate"
echo "2. Ejecuta: python manage.py runserver"
echo "3. Prueba las URLs:"
echo "   - http://localhost:8000/accounts/signup/"
echo "   - http://localhost:8000/accounts/login/"
echo "   - http://localhost:8000/accounts/password-reset/"
echo ""
echo "Para ver emails de recuperación, revisa la consola donde"
echo "corre el servidor de desarrollo."
echo ""
