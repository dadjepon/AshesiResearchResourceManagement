from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from datetime import datetime
from django.utils import timezone
from Account.models import UserAccount


class AcademicYear(models.Model):
    """
    defines attributes for an academic year class

    Attributes:
        - start_year: starting year of academic year
        - end_year: ending year of academic year
    """

    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    start_year = models.IntegerField(validators=[MaxValueValidator(datetime.now().year)])
    end_year = models.IntegerField(validators=[MaxValueValidator(datetime.now().year)])
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.start_year}-{self.end_year}"
    
    @classmethod
    def mark_completed(cls):
        """
        marks all academic years as completed if the current year is greater than the end year
        """
        cls.objects.filter(end_year__lt=timezone.now().year).update(is_completed=True)


class SemesterChoices(models.TextChoices):
    """
    defines choices for semester types
    types: (Fall, Winter, Spring, Summer)
    """

    Fall = "Fall", _("Fall")
    Winter = "Winter", _("Winter")
    Spring = "Spring", _("Spring")
    Summer = "Summer", _("Summer")


class Semester(models.Model):
    """
    defines attributes for a semester class

    Attributes:
        - year: academic year
        - semester: semester (Fall, Winter, Spring, Summer)
        - start_date: starting date of semester
        - end_date: ending date of semester
    """

    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    semester = models.CharField(max_length=100, choices=SemesterChoices.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.year} {self.semester}"
    
    @classmethod
    def mark_completed(cls):
        """
        marks all semesters as completed if the current date is greater than the end date
        """
        cls.objects.filter(end_date__lt=timezone.now().date()).update(is_completed=True)