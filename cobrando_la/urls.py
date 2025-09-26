from django.contrib import admin
from django.urls import path
from bank_details.views import public_profile

urlpatterns = [
    path("admin/", admin.site.urls),
    path("u/<slug:public_slug>/", public_profile, name="public_profile"),
]
