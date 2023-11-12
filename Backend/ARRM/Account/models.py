from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from datetime import timedelta


class CustomerAccountManager(BaseUserManager):

    def create_user(self, employee_id, firstname, lastname, email, password, **other_fields):

        if not employee_id:
            raise ValueError(_('You must provide an employee id'))
        if not firstname:
            raise ValueError(_('You must provide a firstname'))
        if not lastname:
            raise ValueError(_('You must provide a lastname'))
        if not email:
            raise ValueError(_('You must provide an email address'))
        
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', False)
        other_fields.setdefault('is_superuser', False)

        email = self.normalize_email(email)
        user = self.model(
            employee_id=employee_id, 
            firstname=firstname, 
            lastname=lastname, 
            email=email, 
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, employee_id, firstname, lastname, email, password, **other_fields):

        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        
        return self.create_user(employee_id, firstname, lastname, email, password, **other_fields)

    def create_staffuser(self, employee_id, firstname, lastname, email, password, **other_fields):
            
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', False)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Staffuser must have is_staff=True'))
        if other_fields.get('is_superuser') is not False:
            raise ValueError(_('Staffuser must have is_superuser=False'))
        
        return self.create_user(employee_id, firstname, lastname, email, password, **other_fields)


class Role(models.TextChoices):

    FACULTY = 'FACULTY', _('Faculty')
    RA = 'RA', _('Research Assistant')
    STAFF = 'STAFF', _('Staff')


class UserAccount(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of username

    Attributes:
        - employee_id: Employee ID of the user
        - firstname: Firstname of the user
        - lastname: Lastname of the user
        - email: Email address of the user
        - mobile_number: Mobile number of the user
        - role: Role of the user (whether Faculty or Research Assistant or Staff)
        - nationality: Nationality of the user
        - account_status: Account status of the user (whether disabled or incomplete or complete)
        - is_active: Boolean field to determine if the user is active
        - is_staff: Boolean field to determine if the user is a staff
        - is_superuser: Boolean field to determine if the user is a superuser
    """

    employee_id = models.CharField(primary_key=True, db_index=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    mobile_number = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.RA)
    nationality = models.CharField(max_length=100)
    account_status = models.CharField(max_length=10, default='incomplete')

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomerAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['employee_id', 'firstname', 'lastname', 'mobile_number', 'role']
    
    def __str__(self):
        return f"s{self.employee_id} -> {self.firstname} {self.lastname}"
    
    class Meta:
        verbose_name = 'User Account'
        verbose_name_plural = 'User Accounts'
        ordering = ['-date_joined']
    

class TokenBlacklist(models.Model):
    """
    allows blacklisting of access tokens whose referesh tokens have been revoked

    Attributes:
        - user: Foreign key to the user account whose token is being blacklisted
        - token: The access token to be blacklisted
        - created_at: The date and time the token was blacklisted
    """

    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def is_blacklisted(cls, token):
        return cls.objects.filter(token=token).exists()
    
    @classmethod
    def blacklist(cls, user, token):
        cls.objects.create(user=user, token=token)

    @classmethod
    def clear(cls):
        # clear all tokens older than 1 day
        cls.objects.filter(created_at__lte=timezone.now() - timedelta(days=1)).delete()

    class Meta:
        unique_together = ('user', 'token')
        verbose_name = 'Token Blacklist'
        verbose_name_plural = 'Token Blacklists'
        ordering = ['-created_at']