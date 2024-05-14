from django.urls import path
from . import views

app_name = "mobile_api"

urlpatterns = [
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("reset_password/", views.ResetPasswordView.as_view(), name="reset_password"),
    path("scd_history/", views.SDCHistoryView.as_view(), name="scd_history"),
]