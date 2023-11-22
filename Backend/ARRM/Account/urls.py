from django.urls import path
from .views import RegisterUsersView, AccountLogin
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("premake/", RegisterUsersView.as_view(), name="register_users"),
    path("login/", AccountLogin.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
]