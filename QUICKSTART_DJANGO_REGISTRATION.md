# 🚀 Implementación de django-registration - Guía Rápida

## ✅ ¿Qué se implementó?

Se integró `django-registration-redux` para manejar:

1. **Inicio de sesión** - Usando tu template existente
2. **Registro de usuarios** - Usando tu template existente  
3. **Restablecimiento de contraseña** - Con flujo completo de emails

❌ **NO se implementó activación de cuenta** (según tus requerimientos)

## 📦 Instalación

```bash
# 1. Instalar la librería
pip install django-registration-redux

# 2. Ejecutar migraciones (si hay cambios)
python manage.py migrate

# 3. Ejecutar el servidor
python manage.py runserver
```

## 🧪 Verificación Rápida

```bash
# Ejecutar script de verificación
./verify_django_registration.sh
```

## 🔗 URLs Disponibles

| URL | Descripción |
|-----|-------------|
| `/accounts/login/` | Inicio de sesión |
| `/accounts/logout/` | Cerrar sesión |
| `/accounts/signup/` | Registro de usuario |
| `/accounts/password-reset/` | Solicitar restablecimiento |
| `/accounts/password-reset/done/` | Confirmación de envío |
| `/accounts/reset/<uidb64>/<token>/` | Establecer nueva contraseña |
| `/accounts/reset/done/` | Confirmación de cambio |

## 🎨 Templates Personalizados

Todos los templates mantienen tu diseño con:
- ✨ Glassmorphism effects
- 🌈 Gradientes animados (morado #830AD1 y verde #88BA41)
- 📱 Diseño responsive
- ♿ Accesibilidad completa

### Ubicación de templates:
```
accounts/templates/
├── registration/
│   ├── login.html                     ✓ Existente (adaptado)
│   ├── password_reset.html            ✓ Existente (adaptado)
│   ├── password_reset_done.html       ✨ NUEVO
│   ├── password_reset_confirm.html    ✨ NUEVO
│   ├── password_reset_complete.html   ✨ NUEVO
│   ├── password_reset_email.html      ✨ NUEVO
│   └── password_reset_subject.txt     ✨ NUEVO
└── accounts/
    └── signup.html                     ✓ Existente (adaptado)
```

## 🔧 Configuración Principal

### `settings.py`
```python
INSTALLED_APPS = [
    # ...
    'registration',  # ← AGREGADO
    'accounts',
    # ...
]

# Configuración de django-registration
REGISTRATION_AUTO_LOGIN = True        # Login automático tras registro
REGISTRATION_OPEN = True              # Registro habilitado
ACCOUNT_ACTIVATION_DAYS = 7           # Requerido (aunque no se use)

# Email (en desarrollo muestra en consola)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@cobrando.la'
```

### `accounts/urls.py`
Se configuraron todas las URLs usando:
- `RegistrationView` para registro
- `auth_views` de Django para login/password reset
- Formularios personalizados (`UserCreationForm`, `CustomPasswordResetForm`)

### `accounts/forms.py`
Nuevos formularios:
- `UserCreationForm` - Extiende `RegistrationForm`
  - Soporta email O teléfono
  - Validación personalizada
  - Auto-login tras registro
  
- `CustomPasswordResetForm` - Extiende `PasswordResetForm`
  - Busca usuarios por email
  - Genera token seguro

### `accounts/views.py`
Simplificado drásticamente:
- Solo mantiene `logout_view()`
- Todo lo demás lo maneja django-registration

## 🧪 Cómo Probar

### 1. Registro de Usuario
```bash
# Visitar: http://localhost:8000/accounts/signup/
# - Llenar formulario (email o teléfono + contraseña)
# - Submit
# - Verás que se loguea automáticamente
# - Redirección a /dashboard/
```

### 2. Login
```bash
# Visitar: http://localhost:8000/accounts/login/
# - Ingresar credenciales
# - Submit
# - Redirección a /dashboard/
```

### 3. Password Reset
```bash
# Visitar: http://localhost:8000/accounts/password-reset/
# - Ingresar email
# - Submit
# - Ver email en la CONSOLA del servidor
# - Copiar el enlace del email
# - Pegar en navegador
# - Establecer nueva contraseña
# - Login con nueva contraseña
```

## 📧 Emails en Desarrollo

Los emails se muestran en la **consola** donde ejecutas `runserver`:

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Restablecer contraseña - Cobrando.la
From: noreply@cobrando.la
To: usuario@ejemplo.com

Has solicitado restablecer tu contraseña...
http://localhost:8000/accounts/reset/...
```

## 🚀 Para Producción

En `settings.py`, cambiar:

```python
# Configuración SMTP real
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu-contraseña-de-aplicación'
DEFAULT_FROM_EMAIL = 'noreply@cobrando.la'
```

## 📁 Archivos Modificados

### Nuevos
- ✨ `DJANGO_REGISTRATION_SETUP.md` - Documentación completa
- ✨ `QUICKSTART_DJANGO_REGISTRATION.md` - Esta guía
- ✨ `verify_django_registration.sh` - Script de verificación
- ✨ `accounts/templates/registration/password_reset_done.html`
- ✨ `accounts/templates/registration/password_reset_confirm.html`
- ✨ `accounts/templates/registration/password_reset_complete.html`
- ✨ `accounts/templates/registration/password_reset_email.html`
- ✨ `accounts/templates/registration/password_reset_subject.txt`

### Modificados
- 🔧 `requirements.txt` - Agregado `django-registration-redux>=2.13`
- 🔧 `cobrando_la/settings.py` - Configuración de registration y email
- 🔧 `accounts/urls.py` - Nuevas URLs con vistas de registration
- 🔧 `accounts/views.py` - Simplificado (solo logout)
- 🔧 `accounts/forms.py` - Nuevos formularios que extienden de registration

### Sin cambios
- ✓ `accounts/models.py` - Tu modelo User personalizado funciona perfectamente
- ✓ `accounts/admin.py` - Sigue funcionando igual
- ✓ `accounts/templates/registration/login.html` - Mantiene tu diseño
- ✓ `accounts/templates/registration/password_reset.html` - Mantiene tu diseño
- ✓ `accounts/templates/accounts/signup.html` - Mantiene tu diseño

## 🎯 Beneficios

1. **Código más limpio** - Menos código personalizado que mantener
2. **Más robusto** - Validaciones y seguridad probadas
3. **Extensible** - Fácil agregar funcionalidades en el futuro
4. **Estándar** - Usa patrones de Django establecidos
5. **Mantenible** - Documentación y comunidad activa

## 📚 Documentación Adicional

- Ver `DJANGO_REGISTRATION_SETUP.md` para detalles completos
- [django-registration-redux docs](https://django-registration-redux.readthedocs.io/)
- [Django authentication docs](https://docs.djangoproject.com/en/stable/topics/auth/)

## ❓ Solución de Problemas

### "No module named 'registration'"
```bash
pip install django-registration-redux
```

### Emails no aparecen en consola
Verifica que `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` esté en settings.py

### Error al registrar usuario
Verifica que:
1. Proporcionas email O teléfono (al menos uno)
2. El email/teléfono no esté ya registrado
3. Las contraseñas coincidan

### Token inválido en password reset
El token expira en 24 horas. Solicita un nuevo enlace.

## 🎉 ¡Listo!

Tu sistema de autenticación ahora usa django-registration y mantiene todos tus diseños personalizados.
