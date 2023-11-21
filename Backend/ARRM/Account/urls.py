from django.urls import path
from .views import RegisterUsersView

urlpatterns = [
    path("register/", RegisterUsersView.as_view(), name="register_users"),
]