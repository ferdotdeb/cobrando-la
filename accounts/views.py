from django.contrib.auth import logout, login
from django.shortcuts import redirect, render
from django.views import View
from .forms import UserCreationForm

def logout_view(request):
    """
    Vista personalizada para logout.
    django-registration maneja el signup automáticamente.
    """
    logout(request)
    return redirect("home")


class SignupView(View):
    """
    Vista personalizada de registro que soporta email O teléfono
    """
    template_name = "accounts/signup.html"
    form_class = UserCreationForm
    success_url = "/dashboard/"
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        form = self.form_class()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            # Autenticar e iniciar sesión automáticamente
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(self.success_url)
        
        return render(request, self.template_name, {"form": form})
