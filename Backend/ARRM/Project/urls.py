from django.urls import path
from .views import (
    AddProjectView, RetrieveProjectView, RetrieveProjectsView, UpdateProjectView,
    RemoveProjectStudyAreaView, ChangeProjectVisibilityView, DeleteProjectView, 
    RestoreProjectView, DeleteProjectPermanentlyView,

    RequestProjectMembershipView, RetrieveProjectMembershipRequestsView, 
    AcceptProjectMembershipView, RejectProjectMembershipView, DeleteProjectMembershipRequestView,

    InviteResearchAssistantView, RetrieveProjectInvitationsView, AcceptProjectInvitationView,
    DeclineProjectInvitationView, DeleteProjectInvitationView, 
    
    RetrieveProjectTeamMembersView, RemoveProjectTeamMemberView,

    AddMilestoneView, RetrieveMilestoneView, RetrieveMilestonesView, DeleteMilestoneView,

    RetrieveProjectMilestoneView, RemoveProjectTaskFromMilestoneView, DeleteProjectMilestoneView,

    AddProjectTaskView, RetrieveTaskView, RetrievePendingTasksView, UpdateTaskView, DeleteProjectTaskView,
)

urlpatterns = [
    # PROJECT ROUTES
    path("add/", AddProjectView.as_view(), name="add-project"),
    path("get/<int:project_id>/", RetrieveProjectView.as_view(), name="retrieve-project"),
    path("get/", RetrieveProjectsView.as_view(), name="retrieve-projects"),
    path("update/<int:project_id>/", UpdateProjectView.as_view(), name="update-project"),
    path("study_area/remove/", RemoveProjectStudyAreaView.as_view(), name="remove-project-study-area"),
    path("visibility/change/<int:project_id>/", ChangeProjectVisibilityView.as_view(), name="change-project-visibility"),
    path("delete/<int:project_id>/", DeleteProjectView.as_view(), name="delete-project"),
    path("restore/<int:project_id>/", RestoreProjectView.as_view(), name="restore-project"),
    path("delete/permanently/<int:project_id>/", DeleteProjectPermanentlyView.as_view(), name="delete-project-permanently"),

    # PROJECT TEAM
    path("team/get/<int:project_id>/", RetrieveProjectTeamMembersView.as_view(), name="retrieve-project-team-members"),
    path("team/remove/<int:project_member_id>/", RemoveProjectTeamMemberView.as_view(), name="remove-project-team-member"),

    # PROJECT MEMBERSHIP ROUTES
    path("membership/request/<int:project_id>/", RequestProjectMembershipView.as_view(), name="request-project-membership"),
    path("membership/request/get/<int:project_id>/", RetrieveProjectMembershipRequestsView.as_view(), name="retrieve-project-membership-requests"),
    path("membership/request/accept/<int:project_request_id>/", AcceptProjectMembershipView.as_view(), name="accept-project-membership-request"),
    path("membership/request/reject/<int:project_request_id>/", RejectProjectMembershipView.as_view(), name="reject-project-membership-request"),
    path("membership/request/delete/<int:project_request_id>/", DeleteProjectMembershipRequestView.as_view(), name="delete-project-membership-request"),

    # PROJECT INVITATION ROUTES
    path("invitation/invite/", InviteResearchAssistantView.as_view(), name="invite-research-assistant"),
    path("invitation/get/<int:project_id>/", RetrieveProjectInvitationsView.as_view(), name="retrieve-project-invitations"),
    path("invitation/accept/<int:project_invite_id>/", AcceptProjectInvitationView.as_view(), name="accept-project-invitation"),
    path("invitation/decline/<int:project_invite_id>/", DeclineProjectInvitationView.as_view(), name="reject-project-invitation"),
    path("invitation/delete/<int:project_invite_id>/", DeleteProjectInvitationView.as_view(), name="delete-project-invitation"),

    # MILESTONE ROUTES
    path("milestone/add/", AddMilestoneView.as_view(), name="add-milestone"),
    path("milestone/get/<int:milestone_id>/", RetrieveMilestoneView.as_view(), name="retrieve-milestone"),
    path("milestone/get/", RetrieveMilestonesView.as_view(), name="retrieve-milestones"),
    path("milestone/delete/<int:milestone_id>/", DeleteMilestoneView.as_view(), name="delete-milestone"),

    # PROJECT MILESTONE AND TASK ROUTES
    path("project_milestone/get/<int:project_milestone_id>/", RetrieveProjectMilestoneView.as_view(), name="retrieve-project-milestone"),
    path("project_milestone/task/remove/", RemoveProjectTaskFromMilestoneView.as_view(), name="remove-project-task-from-milestone"),
    path("project_milestone/delete/<int:project_milestone_id>/", DeleteProjectMilestoneView.as_view(), name="delete-project-milestone"),
    
    path("task/add/<int:project_id>/", AddProjectTaskView.as_view(), name="add-task"),
    path("task/get/<int:task_id>/", RetrieveTaskView.as_view(), name="retrieve-task"),
    path("task/get/pending/", RetrievePendingTasksView.as_view(), name="retrieve-pending-tasks"),
    path("task/update/<int:task_id>/", UpdateTaskView.as_view(), name="update-task"),
    path("task/delete/<int:task_id>/", DeleteProjectTaskView.as_view(), name="delete-task"),
]