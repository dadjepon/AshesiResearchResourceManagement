from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from datetime import datetime

from Account.models import UserAccount
from .helper import (transcript_upload_path, sample_upload_path, profile_picture_upload_path,
                     cv_upload_path)


class DegreeType(models.TextChoices):
    """
    defines choices for degree types
    types: (BSc, MSc, PhD)
    """

    AA = "AA", _("Associate of Arts")
    AS = "AS", _("Associate of Science")
    BA = "BA", _("Bachelor of Arts")
    BSc = "BSc", _("Bachelor of Science")
    BFA = "BFA", _("Bachelor of Fine Arts")
    LLB = "LLB", _("Bachelor of Laws")
    LLM = "LLM", _("Master of Laws")
    JD = "JD", _("Juris Doctor")
    BCL = "BCL", _("Bachelor of Civil Law")
    BLS = "BLS", _("Bachelor of Legal Studies")
    BPhil = "BPhil", _("Bachelor of Philosophy")
    BEng = "BEng", _("Bachelor of Engineering")
    BEd = "BEd", _("Bachelor of Education")
    MA = "MA", _("Master of Arts")
    MSc = "MSc", _("Master of Science")
    MBA = "MBA", _("Master of Business Administration")
    PhD = "PhD", _("Doctor of Philosophy")
    EdD = "EdD", _("Doctor of Education")
    MD = "MD", _("Doctor of Medicine")
    EdS = "EdS", _("Education Specialist")
    EngD = "EngD", _("Doctor of Engineering")
    PsyD = "PsyD", _("Doctor of Psychology")
    DMA = "DMA", _("Doctor of Musical Arts")


class Degree(models.Model):
    """
    defines attributes for a degree class

    Attributes:
        - user (UserAccount): the user's account
        - type (CharField): type of degree
        - university (CharField): university of degree
        - major (CharField): major of degree
        - graduation_year (IntegerField): year of graduation
        - transcript (FileField): degree transcript
        - created_at (DateTimeField): date degree was created
    """

    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=DegreeType.choices)
    university = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    graduation_year = models.IntegerField(validators=[MaxValueValidator(datetime.now().year)])
    transcript = models.FileField(upload_to=transcript_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type} in {self.major} from {self.university} - {self.graduation_year}"


class WritingSample(models.Model):
    """
    defines attributes for a writing sample class

    Attributes:
        - user (UserAccount): the user's account
        - title (CharField): title of writing sample
        - publication_link (CharField): link to publication
        - sample (FileField): writing sample
        - created_at (DateTimeField): date writing sample was created
    """

    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    publication_link = models.CharField(max_length=250, blank=True, null=True)
    sample = models.FileField(upload_to=sample_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Interest(models.Model):
    """
    defines attributes for an interest class

    Attributes:
        - name: name of interest
        - study_area: study area of interest
    """

    name = models.CharField(max_length=100, unique=True)
    study_area = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name} : {self.study_area}"


class ResearchAssistant(models.Model):
    """
    defines attributes for a research assistant class

    Attributes:
        - user (UserAccount): the user's account
        - bio (TextField): the user's bio
        - profile_picture (ImageField): the user's profile picture
        - interests (ManyToManyField): the user's interests
        - linkedin_url (CharField): the user's linkedin url
        - cv (FileField): the user's cv
    """

    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to=profile_picture_upload_path, blank=True, null=True)
    interests = models.ManyToManyField(Interest, blank=True, null=True)
    linkedin_url = models.CharField(max_length=250, blank=True, null=True)
    cv = models.FileField(upload_to=cv_upload_path, blank=True, null=True)

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname} - {self.linkedin_url}"
    

class Faculty(models.Model):
    """
    defines attributes for a faculty class

    Attributes:
        - user (UserAccount): the user's account
        - bio (TextField): the user's bio
        - profile_picture (ImageField): the user's profile picture
        - department (CharField): the user's department
        - interests (ManyToManyField): the user's interests
    """

    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to=profile_picture_upload_path, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    interests = models.ManyToManyField(Interest, blank=True, null=True)

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname} - {self.department}"