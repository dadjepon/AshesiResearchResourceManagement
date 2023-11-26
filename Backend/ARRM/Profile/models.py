from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from datetime import datetime

from Account.models import UserAccount
from .helper import transcript_upload_path, sample_upload_path


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
    defines attributes for a degree model

    Attributes:
        - user: user's account
        - type: degree type (BSc, MSc, PhD)
        - university: name of university
        - major: major of degree
        - graduation_year: year of graduation
        - transcript: degree transcript
        - created_at: date degree was created
    """

    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=DegreeType.choices)
    university = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    graduation_year = models.IntegerField(validators=[MaxValueValidator(datetime.now().year)])
    transcript = models.FileField(upload_to=transcript_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    # is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.type


class WritingSample(models.Model):
    """
    defines attributes for a writing sample model

    Attributes:
        - user: user's account
        - title: title of writing sample
        - publication_link: link to publication
        - sample: writing sample
        - created_at: date writing sample was created
    """

    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    publication_link = models.CharField(max_length=100, blank=True, null=True)
    sample = models.FileField(upload_to=sample_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title