from rest_framework import serializers

from .models import UserAccount, Role, TokenBlacklist


class AccountRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = [
            "employee_id", "firstname", "lastname", "email",
            "mobile_number", "role", "nationality", "last_login"
        ]


class UserAccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserAccount
        fields = [
            "employee_id", "firstname", "lastname", "email",
            "mobile_number", "role", "nationality", "last_login"
        ]