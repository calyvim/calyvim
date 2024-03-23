from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("calyvim.urls.accounts")),
    path("dashboard/", include("calyvim.urls.dashboard")),
    path("", include("calyvim.urls.home"))
]
