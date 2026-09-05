from django.urls import path
from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.home, name="home"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path(
    "resume/download/<int:resume_id>/",
    views.download_resume,
    name="download_resume",
),
]