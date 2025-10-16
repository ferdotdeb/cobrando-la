from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from .forms import UserCreationForm

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # login inmediato tras registro
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")

def password_reset_request(request):
    """
    Vista para solicitar el restablecimiento de contraseña.
    Por el momento solo muestra el template sin funcionalidad.
    """
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        # TODO: Implementar lógica de envío de email
        # Por ahora solo renderiza el form
    else:
        form = PasswordResetForm()
    return render(request, "registration/password_reset.html", {"form": form})
