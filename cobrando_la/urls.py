from django.contrib import admin
from django.urls import path, include
from bank_details.views import public_profile
from home.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", index, name="home"),  # Landing Page
    path("dashboard/", include("bank_details.urls")),  # Dashboard
    path("u/<slug:public_slug>/", public_profile, name="public_profile"),
]