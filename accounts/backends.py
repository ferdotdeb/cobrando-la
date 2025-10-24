from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailOrPhoneBackend(ModelBackend):
    """
    Backend de autenticación personalizado que permite login con email o teléfono
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        try:
            # Intentar buscar por email primero
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                # Si no tiene @, asumir que es teléfono
                user = User.objects.get(phone=username)
        except User.DoesNotExist:
            # Ejecutar el hasher de contraseña por defecto para evitar timing attacks
            User().set_password(password)
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
