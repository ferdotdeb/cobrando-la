from django.contrib import admin
from django.urls import path, include
from bank_details.views import public_profile  # ya lo tienes

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("bank_details.urls")),  # dashboard
    path("u/<slug:public_slug>/", public_profile, name="public_profile"),
]
