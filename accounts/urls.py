from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup, logout_view, password_reset_request

urlpatterns = [
    path("login/",  auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup/", signup, name="signup"),
    path("password-reset/", password_reset_request, name="password_reset"),
]
