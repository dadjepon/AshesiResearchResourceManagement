from cProfile import label
import email
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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


class AccountLoginSerializer(TokenObtainPairSerializer):
    """
    defines a custom token obtain pair serializer which allows
    users to login with their email and password
    """
    
    email = serializers.EmailField(
        write_only=True, 
        required=True,
        validators=[EMAIL_REGEX]
    )
    password = serializers.CharField(
        write_only=True, 
        required=True,
        trim_whitespace=False,
        label="Password",
        style={"input_type": "password"},
        validators=[PASSWORD_REGEX]
    )
    token = serializers.SerializerMethodField("get_token")

    class Meta:
        model = UserAccount
        fields = ["email", "password", "token"]
        extra_kwargs = {
            "access": {"read_only": True},
            "refresh": {"read_only": True}
        }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # add user's firstname, lastname and role to token payload
        token["firstname"] = user.firstname # type: ignore
        token["lastname"] = user.lastname # type: ignore
        token["role"] = user.role # type: ignore
        return token
    
    def validate_email(self, value):
        return re.match(EMAIL_REGEX, value)
    
    def validate_password(self, value):
        return re.match(PASSWORD_REGEX, value)
    
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = UserAccount.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("No user found with this email!")
        
        if not user.check_password(password): # type: ignore
            raise serializers.ValidationError("Invalid email or password!")
        
        if not user.is_active:
            raise serializers.ValidationError("Account is disabled!")
        
        user_data = UserAccountSerializer(user).data
        token = self.get_token(user) # type: ignore
        user_data["refresh_token"] = str(token)
        user_data["access_token"] = str(token.access_token) # type: ignore
        return user_data
    
    default_error_messages = {
        "no_active_account": "No active account found with the given credentials"
    }