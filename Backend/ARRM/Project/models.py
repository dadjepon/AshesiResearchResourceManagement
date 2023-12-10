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


class ProjectTeam(models.Model):
    """
    defines attributes for a ProjectTeam class

    Attributes:
        - project (Project): the project
        - user (UserAccount): the user account of the team member
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project.title} -> {self.user.email}"


class ProjectTeamRequest(models.Model):
    """
    defines attributes for a ProjectTeamRequest class

    Attributes:
        - project (Project): the project
        - user (UserAccount): the requesting user's account
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project.title} -> {self.user.email}"
    

class ProjectTeamInvitation(models.Model):
    """
    defines attributes for a ProjectTeamInvitation class

    Attributes:
        - project (Project): the project
        - user (UserAccount): the invited user's account
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project.title} -> {self.user.email}"


class Milestone(models.Model):
    """
    defines attributes for a Milestone class

    Attributes:
        - name (CharField): the milestone's name
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class ProjectMilestoneTemplate(models.TextChoices):
    """
    defines choices for project milestone templates
    E.g. standard, project planning, literature review, data collection and processing etc.
    """
    
    STANDARD = "standard", _("Standard")
    PROJECT_PLANNING = "project_planning", _("Project Planning")
    LITERATURE_REVIEW = "literature_review", _("Literature Review")
    DATA_COLLECTION_AND_PROCESSING = "data_collection_and_processing", _("Data Collection and Processing")
    DISSEMINATION = "dissemination", _("Dissemination")


class ProjectMilestone(models.Model):
    """
    defines attributes for a ProjectMilestone class

    Attributes:
        - project (Project): the project
        - milestone (Milestone): the milestone
        - status (CharField): the milestone's status
        - due_date (DateField): the milestone's due date
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project.title} -> {self.milestone.name}"
    

class ProjectTask(models.Model):
    """
    defines attributes for a ProjectTask class

    Attributes:
        - project_milestone (ProjectMilestone): the project milestone
        - assignee (UserAccount): the RA or Faculty assigned to the task
        - name (CharField): the task's name
        - description (TextField): the task's description
        - status (CharField): the task's status
        - hours_required (IntegerField): the number of hours required to complete the task
        - due_date (DateField): the task's due date
    """
    
    project_milestone = models.ForeignKey(ProjectMilestone, on_delete=models.CASCADE)
    assignee = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.TODO)
    hours_required = models.IntegerField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.project_milestone.project.title} : {self.project_milestone.milestone.name} - {self.name}"


class ProjectTaskFeedback(models.Model):
    """
    defines attributes for a ProjectTaskFeedback class

    Attributes:
        - project_task (ProjectTask): the project task
        - reviewer (UserAccount) : the user who is reviewing the task
        - target_member (UserAccount): the Project member who is being reviewed
        - feedback (TextField): the task's feedback
        - created_at (DateTimeField): the task's creation date
    """

    project_task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="reviewer")
    target_member = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="target_member")
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project_task.name} : {self.target_member.email} - {self.project_task.name}"