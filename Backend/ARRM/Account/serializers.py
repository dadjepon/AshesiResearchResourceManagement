from rest_framework import serializers
from .models import UserAccount, Role
from .helper import read_country_file


class RegistrationSerializer(serializers.ModelSerializer):
    COUNTRY_CODES = read_country_file()

    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, 
        write_only=True
    )

    class Meta:
        model = UserAccount
        fields = [
            'employee_id', 'firstname', 'lastname', 'email', 'password', 
            'confirm_password', 'mobile_number', 'role', 'nationality'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True, 
                'style': {'input_type': 'password'}
            },
        }

    def validate_employee_id(self, value):
        if UserAccount.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError('Employee ID already exists!')
        return value

    def validate_firstname(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('Firstname must only contain letters!')
        return value
    
    def validate_lastname(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('Lastname must only contain letters!')
        return value
    
    def validate_email(self, value):
        if UserAccount.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists!')

        # NB: update this to proper email regex validation
        if not value.endswith('@ashesi.edu.gh'):
            raise serializers.ValidationError('Email must be an Ashesi email!')

        return value
    
    def validate_nationality(self, value):
        if value.lower() not in self.COUNTRY_CODES.keys():
            raise serializers.ValidationError('{value} is not valid country!')
    
    # NB: should we assume the user will always enter a mobile number with the right country code?
    def validate_mobile_number(self, value):
        if UserAccount.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError('An account with this mobile number already exists!')

    def validate_role(self, value):
        if value.upper() not in Role.choices:
            raise serializers.ValidationError('Role must be either Faculty, Research Assistant or Staff!')
        return value
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password': 'Passwords must match!'})
        return data
    
    def create(self, validated_data):
        return UserAccount.objects.create(**validated_data)
    
    def save(self):
        user = UserAccount(
            employee_id=self.validated_data['employee_id'],
            firstname=self.validated_data['firstname'],
            lastname=self.validated_data['lastname'],
            email=self.validated_data['email'],
            mobile_number=self.validated_data['mobile_number'],
            role=self.validated_data['role'],
            nationality=self.validated_data['nationality']
        )

        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Passwords must match!'})
        
        user.set_password(password)
        user.save()
        return user