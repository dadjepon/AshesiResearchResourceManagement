from math import e
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import UserAccount, Status, Role, TokenBlacklist
from .helper import EMAIL_REGEX, PASSWORD_REGEX
import re
from Profile.models import Faculty, ResearchAssistant
from Profile.serializers import FacultySerializer, ResearchAssistantSerializer


class AccountRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True
    )
    confirm_password = serializers.CharField(
        write_only=True, 
        required=True
    )

    class Meta:
        model = UserAccount
        fields = [
            "id", "firstname", "lastname", "email", "password", "confirm_password",
            "mobile_number", "role", "nationality", "last_login", "account_status"
        ]

    def validate_id(self, value):        
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
        if not re.match(EMAIL_REGEX, value):
            raise serializers.ValidationError("Invalid email address")
        
        if UserAccount.objects.filter(email=value).exists():
            raise serializers.ValidationError("An account with this email already exists!")
        
        return value
    
    def validate_password(self, value):
        if not re.match(PASSWORD_REGEX, value):
            raise serializers.ValidationError("Invalid password")
        
        return value
    
    def validate_confirm_password(self, value):
        if not re.match(PASSWORD_REGEX, value):
            raise serializers.ValidationError("Invalid password")
        
        return value
    
    def validate_mobile_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Mobile number must contain only numbers")
        
        if UserAccount.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("An account with this mobile number already exists!")
        
        return value
    
    def validate_role(self, value):
        if value not in Role.values:
            raise serializers.ValidationError("Invalid role")
        
        return value
    
    def validate_account_status(self, value):
        if value not in Status.values:
            raise serializers.ValidationError("Invalid account status!")
        
        return value

    def create(self, **validated_data):      
        return UserAccount.objects.create(**validated_data)
    
    def save(self):
        user_account = UserAccount(
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
            "id", "firstname", "lastname", "email",
            "mobile_number", "role", "nationality", "last_login"
        ]

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)

    #     # extend Faculty or ResearchAssistant representation
    #     if instance.role == Role.FACULTY:
    #         if Faculty.objects.filter(user=instance).exists():
    #             extended_rep = FacultySerializer(Faculty.objects.get(user=instance), context=self.context).data
    #         else:
    #             extended_rep = {}
    #     elif instance.role == Role.RA:
    #         if ResearchAssistant.objects.filter(user=instance).exists():
    #             extended_rep = ResearchAssistantSerializer(ResearchAssistant.objects.get(user=instance), context=self.context).data
    #         else:
    #             extended_rep = {}
    #     else:
    #         extended_rep = {}

    #     representation.update(extended_rep)
    #     return representation


class AccountLoginSerializer(TokenObtainPairSerializer):
    """
    defines a custom token obtain pair serializer which allows
    users to login with their email and password
    """
    
    email = serializers.EmailField(
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
        if re.match(EMAIL_REGEX, value):
            return value
        
        raise serializers.ValidationError("Invalid email address")
    
    # def validate_password(self, value):
    #     if re.match(PASSWORD_REGEX, value):
    #         return value
        
    #     raise serializers.ValidationError("Password does not match required format.")
    
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = UserAccount.objects.get(email=email)
        if user is None:
            raise serializers.ValidationError("No user found with this email!")
        
        if not user.check_password(password): # type: ignore
            raise serializers.ValidationError("Incorrect password!")
        
        if not user.is_active:
            raise serializers.ValidationError("Account is disabled!")
        
        token = self.get_token(user) # type: ignore
        user_data = UserAccountSerializer(user).data
        user_data["refresh_token"] = str(token)
        user_data["access_token"] = str(token.access_token) # type: ignore
        return user_data
    

class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect password!")
        
        if not re.match(PASSWORD_REGEX, value):
            raise serializers.ValidationError("Invalid password")
        
        return value
    
    def validate_new_password(self, value):
        if not re.match(PASSWORD_REGEX, value):
            raise serializers.ValidationError("Invalid password")
        
        return value
    
    def validate_confirm_password(self, value):
        if not re.match(PASSWORD_REGEX, value):
            raise serializers.ValidationError("Invalid password")
        
        return value
    
    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        
        if attrs["old_password"] == attrs["new_password"]:
            raise serializers.ValidationError("New password cannot be the same as old password!")
        
        validate_password(attrs["new_password"], user=self.context["request"].user)
        return attrs
    
    def update(self, instance, validated_data):
        user = self.context["request"].user

        if user.pk != instance.pk:
            raise serializers.ValidationError("You do not have permission for this user!")
        
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance