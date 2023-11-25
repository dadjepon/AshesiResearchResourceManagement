from django.urls import path
from .views import (RegisterUsersView, AccountLogin, AccountView, ChangePasswordView,
                    AccountLogoutView, DeleteAccountView)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("premake/", RegisterUsersView.as_view(), name="register-users"),
    path("login/", AccountLogin.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("user/", AccountView.as_view(), name="user-details"),
    path("change_password/<int:pk>/", ChangePasswordView.as_view(), name="change-password"),
    path("logout/", AccountLogoutView.as_view(), name="logout"),
    path("delete/<int:user_id>/", DeleteAccountView.as_view(), name="delete-account")
]