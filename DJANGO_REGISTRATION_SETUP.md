# Implementación de django-registration-redux

## Resumen de Cambios

Se ha implementado `django-registration-redux` en el proyecto para gestionar de manera más robusta:
- ✅ Inicio de sesión
- ✅ Registro de usuario
- ✅ Restablecimiento de contraseña

**NOTA:** No se implementó activación de cuenta ya que no es necesaria para esta aplicación.

## Instalación

### 1. Dependencias
Se agregó a `requirements.txt`:
```
django-registration-redux>=2.13
```

Para instalar:
```bash
pip install -r requirements.txt
```

## Configuración

### 2. Settings (`cobrando_la/settings.py`)

Se agregó `registration` a `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ...
    'registration',  # django-registration-redux
    'accounts',
    # ...
]
```

Se agregaron las siguientes configuraciones:
```python
# django-registration-redux settings
ACCOUNT_ACTIVATION_DAYS = 7  # Requerido pero no se usa
REGISTRATION_AUTO_LOGIN = True  # Login automático después del registro
REGISTRATION_OPEN = True  # El registro está abierto

# Configuración de email (para reset de contraseña)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # En desarrollo
DEFAULT_FROM_EMAIL = 'noreply@cobrando.la'
```

**Para producción**, cambiar a SMTP real:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu-contraseña-de-aplicación'
```

## Estructura de Archivos

### 3. Formularios (`accounts/forms.py`)

#### UserCreationForm
Extiende de `RegistrationForm` de django-registration:
- Soporta email O teléfono (al menos uno requerido)
- Validación de contraseñas coincidentes
- Validación de unicidad de email y teléfono
- Auto-login después del registro (configurado en settings)

#### CustomPasswordResetForm
Formulario personalizado para reset de contraseña:
- Busca usuarios por email
- Solo permite reset para usuarios activos con contraseña usable

### 4. Vistas (`accounts/views.py`)

Se simplificó significativamente, ahora solo contiene:
- `logout_view`: Vista personalizada para logout

**django-registration maneja automáticamente:**
- Registro de usuario (usando `RegistrationView`)
- Login (usando vistas de Django auth)
- Password reset (usando vistas de Django auth)

### 5. URLs (`accounts/urls.py`)

Configuración completa de URLs:

```python
/accounts/login/              -> Login
/accounts/logout/             -> Logout
/accounts/signup/             -> Registro
/accounts/password-reset/     -> Solicitar reset
/accounts/password-reset/done/ -> Confirmación de envío
/accounts/reset/<uidb64>/<token>/ -> Establecer nueva contraseña
/accounts/reset/done/         -> Confirmación de cambio exitoso
```

## Templates

### 6. Templates de Autenticación

Todos los templates mantienen el diseño existente con glassmorphism y gradientes:

#### `/accounts/templates/registration/`
- `login.html` - **EXISTENTE** (adaptado)
- `password_reset.html` - **EXISTENTE** (adaptado)
- `password_reset_done.html` - **NUEVO** ✨
- `password_reset_confirm.html` - **NUEVO** ✨
- `password_reset_complete.html` - **NUEVO** ✨
- `password_reset_email.html` - **NUEVO** ✨
- `password_reset_subject.txt` - **NUEVO** ✨

#### `/accounts/templates/accounts/`
- `signup.html` - **EXISTENTE** (adaptado)

## Flujo de Usuario

### Registro de Usuario
1. Usuario visita `/accounts/signup/`
2. Completa el formulario (email O teléfono + contraseña)
3. `RegistrationView` procesa el formulario con `UserCreationForm`
4. Usuario se crea y se loguea automáticamente (REGISTRATION_AUTO_LOGIN=True)
5. Redirección a `/dashboard/`

### Inicio de Sesión
1. Usuario visita `/accounts/login/`
2. Ingresa credenciales (email/teléfono + contraseña)
3. Django auth views procesa el login
4. Redirección a `LOGIN_REDIRECT_URL` (/dashboard/)

### Restablecimiento de Contraseña
1. Usuario visita `/accounts/password-reset/`
2. Ingresa su email
3. Sistema envía email con token único
4. Usuario hace clic en enlace del email
5. Visita `/accounts/reset/<uidb64>/<token>/`
6. Ingresa nueva contraseña
7. Redirección a `/accounts/reset/done/`
8. Usuario puede hacer login con nueva contraseña

## Características Especiales

### Modelo de Usuario Personalizado
- Soporta login con **email O teléfono**
- Genera `public_slug` automáticamente para perfiles públicos
- Validación a nivel de modelo y base de datos

### Seguridad
- Tokens de reset expiran automáticamente
- Contraseñas hasheadas con PBKDF2
- CSRF protection en todos los formularios
- Validación de contraseñas (longitud, similitud, común)

### Accesibilidad y UX
- Focus visible en todos los elementos interactivos
- Respeta `prefers-reduced-motion`
- Diseño responsive (móvil primero)
- Mensajes de error claros y específicos

## Testing

Para probar el sistema completo:

### 1. Registro
```bash
python manage.py runserver
# Visitar: http://localhost:8000/accounts/signup/
```

### 2. Login
```bash
# Visitar: http://localhost:8000/accounts/login/
```

### 3. Password Reset (desarrollo)
```bash
# Visitar: http://localhost:8000/accounts/password-reset/
# El email se mostrará en la consola donde corre el servidor
```

## Comandos Útiles

### Crear superusuario
```bash
python manage.py createsuperuser
```

### Ver emails en consola (desarrollo)
Ya está configurado en settings.py con:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Migrar base de datos
```bash
python manage.py makemigrations
python manage.py migrate
```

## Ventajas de django-registration-redux

1. **Manejo robusto de registro**: Validación incorporada, backends configurables
2. **Flexibilidad**: Fácil personalizar formularios y vistas
3. **Seguridad**: Mejores prácticas incluidas por defecto
4. **Mantenibilidad**: Menos código personalizado que mantener
5. **Extensibilidad**: Fácil agregar activación de cuenta en el futuro si se necesita

## Diferencias con Implementación Anterior

### Antes
- Vista personalizada `signup()` en views.py
- Vista stub `password_reset_request()` sin funcionalidad
- No había flujo completo de password reset

### Ahora
- `RegistrationView` de django-registration maneja signup
- Flujo completo de password reset con emails funcionales
- Formularios con validación robusta
- Código más limpio y mantenible

## Próximos Pasos (Opcional)

Si en el futuro necesitas:

### Activación por Email
Cambiar en `accounts/urls.py`:
```python
from registration.backends.default.views import RegistrationView

# En lugar de registration.backends.simple
```

Y configurar:
```python
# settings.py
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = False
```

### Personalizar Emails HTML
Crear versión HTML de `password_reset_email.html` con diseño completo.

### Agregar OAuth (Google, Facebook, etc.)
Integrar `django-allauth` que es compatible con django-registration.

## Soporte

Para más información:
- [django-registration-redux docs](https://django-registration-redux.readthedocs.io/)
- [Django auth docs](https://docs.djangoproject.com/en/stable/topics/auth/)
