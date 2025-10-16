from django.urls import path, include
from django.contrib.auth import views as auth_views
from registration.backends.simple.views import RegistrationView
from .views import logout_view
from .forms import UserCreationForm, CustomPasswordResetForm

urlpatterns = [
    # Login personalizado (usando el template existente)
    path("login/", auth_views.LoginView.as_view(
        template_name="registration/login.html"
    ), name="login"),
    
    # Logout personalizado
    path("logout/", logout_view, name="logout"),
    
    # Registro usando django-registration con nuestro formulario personalizado
    path("signup/", RegistrationView.as_view(
        form_class=UserCreationForm,
        template_name="accounts/signup.html",
        success_url="/dashboard/"
    ), name="signup"),
    
    # Password reset views (usando templates personalizados)
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset.html",
        email_template_name="registration/password_reset_email.html",
        subject_template_name="registration/password_reset_subject.txt",
        form_class=CustomPasswordResetForm,
        success_url="/accounts/password-reset/done/"
    ), name="password_reset"),
    
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"
    ), name="password_reset_done"),
    
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html",
        success_url="/accounts/reset/done/"
    ), name="password_reset_confirm"),
    
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"
    ), name="password_reset_complete"),
]
