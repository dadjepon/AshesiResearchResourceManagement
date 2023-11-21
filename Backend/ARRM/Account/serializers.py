from rest_framework import serializers
from .models import UserAccount, Role, TokenBlacklist
from .helper import EMAIL_REGEX, PASSWORD_REGEX
import re


class AccountRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[PASSWORD_REGEX])
    confirm_password = serializers.CharField(write_only=True, required=True, validators=[PASSWORD_REGEX])

    class Meta:
        model = UserAccount
        fields = [
            "employee_id", "firstname", "lastname", "email",
            "mobile_number", "role", "nationality", "last_login"
        ]

    def validate_employee_id(self, value):        
        if not value.isdigit():
            raise serializers.ValidationError("Employee ID must be a number")
        
        return value
    
    def validate_firstname(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("First name must contain only letters")
        
        return value
    
    def validate_lastname(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Last name must contain only letters")
        
        return value
    
    def validate_email(self, value):
        return re.match(EMAIL_REGEX, value)
    
    def validate_mobile_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Mobile number must contain only numbers")
        
        return value
    
    def validate_role(self, value):
        if value not in Role.values:
            raise serializers.ValidationError("Invalid role")
        
        return value

    def create(self, **validated_data):      
        return UserAccount.objects.create(**validated_data)
    
    def save(self):
        user_account = UserAccount(
            employee_id=self.validated_data["employee_id"], # type: ignore
            firstname=self.validated_data["firstname"], # type: ignore
            lastname=self.validated_data["lastname"], # type: ignore
            email=self.validated_data["email"], # type: ignore
            mobile_number=self.validated_data["mobile_number"], # type: ignore
            role=self.validated_data["role"], # type: ignore
            nationality=self.validated_data["nationality"] # type: ignore
        )
        
        password = self.validated_data["password"] # type: ignore
        confirm_password = self.validated_data["confirm_password"] # type: ignore

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        else:
            user_account.set_password(password)
            user_account.save()
            return user_account        


class UserAccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserAccount
        fields = [
            "employee_id", "firstname", "lastname", "email",
            "mobile_number", "role", "nationality", "last_login"
        ]