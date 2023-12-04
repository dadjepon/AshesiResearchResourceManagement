from django.db import models
from django.utils.translation import gettext_lazy as _

from Account.models import UserAccount
from Profile.models import StudyArea


class ProjectStatus(models.TextChoices):
    """
    defines choices for project status
    types: (pending, in-progress, completed, anulled)
    """

    PENDING = "pending", _("Pending")
    IN_PROGRESS = "in_progress", _("In Progress")
    TODO = "todo", _("To Do")
    IN_REVIEW = "in_review", _("In Review")
    DONE = "done", _("Done")
    COMPLETED = "completed", _("Completed")
    ANULLED = "anulled", _("Anulled")


class Project(models.Model):
    """
    defines attributes for a Project class

    Attributes:
        - user (UserAccount): the user's account
        - title (CharField): the project's title
        - description (TextField): the project's description
        - study_area (ManyToManyField): the project's area of research 
        (normalised to ProjectStudyArea)
        - status (CharField): the project's status
        - start_date (DateField): the project's starting date
        - end_date (DateField): the project's expected ending date
        - visibility (CharField): the project's visibility (public, private)
        - is_deleted (BooleanField): whether the project is deleted or not
        - created_at (DateTimeField): the project's creation date
    """

    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.PENDING)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    visibility = models.CharField(max_length=20, default="private", choices=[("public", "public"), ("private", "private")])
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} -> {self.user.email}"


class ProjectStudyArea(models.Model):
    """
    defines attributes for a ProjectStudyArea class

    Attributes:
        - project (Project): the project
        - study_area (CharField): the project's area of research
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    study_area = models.CharField(max_length=100, choices=StudyArea.choices)

    def __str__(self):
        return f"{self.project.title} -> {self.study_area}"


class Milestone(models.Model):
    """
    defines attributes for a Milestone class

    Attributes:
        - name (CharField): the milestone's name
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name