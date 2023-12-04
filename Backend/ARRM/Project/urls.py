from django.urls import path
from .views import (
    AddProjectView, RetrieveProjectView, RetrieveProjectsView, UpdateProjectView,
    RemoveProjectStudyAreaView, ChangeProjectVisibilityView, DeleteProjectView, 
    RestoreProjectView, DeleteProjectPermanentlyView,

    AddMilestoneView, RetrieveMilestoneView, RetrieveMilestonesView, DeleteMilestoneView,

    AddProjectTaskView,
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

    # MILESTONE ROUTES
    path("milestone/add/", AddMilestoneView.as_view(), name="add-milestone"),
    path("milestone/get/<int:milestone_id>/", RetrieveMilestoneView.as_view(), name="retrieve-milestone"),
    path("milestone/get/", RetrieveMilestonesView.as_view(), name="retrieve-milestones"),
    path("milestone/delete/<int:milestone_id>/", DeleteMilestoneView.as_view(), name="delete-milestone"),

    # PROJECT TASK ROUTES
    path("task/add/<int:project_id>/", AddProjectTaskView.as_view(), name="add-task"),
]