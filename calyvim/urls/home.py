from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path(
        "pricing/",
        TemplateView.as_view(template_name="home/pricing.html"),
        name="pricing",
    ),
    path(
        "features/",
        TemplateView.as_view(template_name="home/features.html"),
        name="features",
    ),
    path("", TemplateView.as_view(template_name="home/index.html"), name="index"),
]
