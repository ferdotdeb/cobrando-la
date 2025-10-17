from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    """
    Vista personalizada para logout.
    django-registration maneja el signup automáticamente.
    """
    logout(request)
    return redirect("home")
