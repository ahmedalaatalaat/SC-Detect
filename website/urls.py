from django.urls import path
from . import views


app_name = "website"

urlpatterns = [
    path("registration/", views.registration_view, name="registration_page"),
    path("history/", views.history_view, name="history_page"),
    path("logout/", views.logout_view, name="logout_page"),
    path("login/", views.login_view, name="login_page"),
    path("", views.home_view, name="home_page"),
]

