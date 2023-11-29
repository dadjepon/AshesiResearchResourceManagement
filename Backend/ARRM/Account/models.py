from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta


class CustomUserManager(BaseUserManager):
    
    def create_user(self, firstname, lastname, email, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        
        other_fields.setdefault('is_staff', False)
        other_fields.setdefault('is_superuser', False)
        other_fields.setdefault('is_active', True)

        email = self.normalize_email(email)
        user = self.model(firstname=firstname, lastname=lastname, email=email, password=password, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, firstname, lastname, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('role', 'admin')
        other_fields.setdefault('account_status', 'complete')
        
        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned to is_staff=True'))
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be assigned to is_superuser=True'))
        
        return self.create_user(firstname, lastname, email, password, **other_fields)


class Role(models.TextChoices):
    """
    defines choices for user roles
    roles: (admin, RA, faculty)
    """
    ADMIN = "admin", _("Admin")
    RA = "ra", _("RA")
    FACULTY = "faculty", _("Faculty")


class Status(models.TextChoices):
    """
    defines choices for user account status
    statuses: (complete, incomplete, suspended)
    """
    COMPLETE = "complete", _("Complete")
    INCOMPLETE = "incomplete", _("Incomplete")
    SUSPENDED = "suspended", _("Suspended")


class UserAccount(AbstractBaseUser, PermissionsMixin):
    """
    defines attributes for a custom user model

    Attributes:
        - firstname (CharField): user's first name
        - lastname (CharField): user's last name
        - email (EmailField): user's email address
        - mobile_number (CharField): user's mobile number
        - role (CharField): user's role (admin, RA, faculty)
        - nationality (CharField): user's nationality
        - account_status (CharField): user's account status (complete, incomplete, suspended)
        - is_staff (BooleanField): user's staff status
        - is_superuser (BooleanField): user's superuser status
        - is_active (BooleanField): user's active status
    """

    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(_('email address'), unique=True)
    mobile_number = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RA)
    nationality = models.CharField(max_length=150)
    account_status = models.CharField(max_length=20, default="incomplete")
    # num_incorrect_logins = models.IntegerField(default=0)
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstname", "lastname", "mobile_number", "nationality"]

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    

class TokenBlacklist(models.Model):
    """
    defines attributes for a token blacklist model

    Attributes:
        - token (CharField): token to be blacklisted
        - blacklisted_at (DateTimeField): date and time token was blacklisted
    """

    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
    
    @classmethod
    def add(cls, token):
        """
        adds a token to the blacklist
        """
        cls.objects.create(token=token)

    @classmethod
    def is_blacklisted(cls, token):
        """
        checks if a token is blacklisted
        """
        return cls.objects.filter(token=token).exists()

    @classmethod
    def cleanup(cls):
        # delete blacklisted tokens older than 24 hours
        cls.objects.filter(blacklisted_at__lte=timezone.now() - timedelta(hours=24)).delete()
    
    class Meta:
        ordering = ["-blacklisted_at"]