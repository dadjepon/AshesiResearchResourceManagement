from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta

from Account.models import UserAccount
from Profile.models import StudyArea


class ProjectStatus(models.TextChoices):
    """
    defines choices for project status
    types: (pending, in-progress, completed, annulled)
    """

    PENDING = "pending", _("Pending")
    IN_PROGRESS = "in_progress", _("In Progress")
    TODO = "todo", _("To Do")
    IN_REVIEW = "in_review", _("In Review")
    DONE = "done", _("Done")
    COMPLETED = "completed", _("Completed")
    ANNULLED = "annulled", _("Annulled")


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
        - estimated_project_hours (FloatField): the project's estimated weekly hours
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
    estimated_project_hours = models.FloatField(blank=True, null=True)
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
    

class TeamMemberRole(models.Model):
    """
    defines attributes for a TeamMemberRole class

    Attributes:
        - user (UserAccount): the user account of the project owner
        - name (CharField): the role's name
    """
    
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProjectRole(models.Model):
    """
    defines attributes for a ProjectRole class

    Attributes:
        - project (Project): the project
        - team_member_role (TeamMemberRole): the role applicable to the project
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    team_member_role = models.ForeignKey(TeamMemberRole, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project.title} -> {self.role.name}"


class ProjectTeam(models.Model):
    """
    defines attributes for a ProjectTeam class

    Attributes:
        - user (UserAccount): the user account of the team member
        - project_role (ProjectRole): the project role for the team member
    """

    project_role = models.ForeignKey(ProjectRole, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project_role.project.title} -> {self.user.email}"


class ProjectTeamRequest(models.Model):
    """
    defines attributes for a ProjectTeamRequest class

    Attributes:
        - project_role (ProjectRole): the project role for the team member
        - user (UserAccount): the requesting user's account
    """

    project_role = models.ForeignKey(ProjectRole, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project_role.project.title} -> {self.user.email}"
    

class ProjectTeamInvitation(models.Model):
    """
    defines attributes for a ProjectTeamInvitation class

    Attributes:
        - project_role (ProjectRole): the project role for the team member
        - user (UserAccount): the invited user's account
    """

    project_role = models.ForeignKey(ProjectRole, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project_role.project.title} -> {self.user.email}"


class ProjectMatchScores(models.Model):
    """
    defines attributes for a ProjectMatch class

    Attributes:
        - project (Project): the project
        - user (UserAccount): the user's account
        - score (FloatField): the user's score
        - created_at (DateTimeField): the match's creation date
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.title} -> {self.user.email} ({self.score}%)"
    
    
    @classmethod
    def clean_matches(cls, project):
        """
        cleans up project matches after 24 hours of match request

        Args:
            - project (Project): the project
        """

        ProjectMatchScores.objects.filter(project=project, created_at__lte=timezone.now() - timedelta(hours=24)).delete()


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
        - assignee (UserAccount): the RA or Faculty assigned to the task    (should be one-to-many, remove and create new model)
        - name (CharField): the task's name
        - description (TextField): the task's description
        - status (CharField): the task's status
        - hours_required (IntegerField): the number of hours required to complete the task
        - due_date (DateField): the task's due date
    """
    
    project_milestone = models.ForeignKey(ProjectMilestone, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.TODO)
    hours_required = models.IntegerField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.project_milestone.project.title} : {self.project_milestone.milestone.name} - {self.name}"
    

class ProjectTaskAssignment(models.Model):
    """
    defines attributes for a ProjectTaskAssignment class to ensure
    more than one user can be assigned to a task

    Attributes:
        - project_task (ProjectTask): the project task
        - assignee (UserAccount): the RA or Faculty assigned to the task
    """

    project_task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE)
    assignee = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project_task.name} -> {self.assignee.email}"


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
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.project_task.name} : {self.target_member.email} - {self.project_task.name}"


class BlindProjectFeedback(models.Model):
    """
    defines attributes for a blind feedback system for a project
    (blind because info about the reviewer isn't returned during query
    but it is stored for permissions handling)

    Attributes:
        - project (Project): the project
        - reviewer (UserAccount): the reviewer
        - intended_user (UserAccount): the user being reviewed
        - rating (FloatField): the rate (out of 5) for the intended_user
        - comment (TextField): the reviewer's comment on the rating
        - time_stamp (DateTimeField): the date the comment was posted
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="reviewer")
    intended_user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="intended_user")
    rating = models.FloatField()
    comment = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.intended_user.firstname} {self.intended_user.lastname} ({self.rating}): {self.comment} at {self.time_stamp}"