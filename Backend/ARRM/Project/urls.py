from django.urls import path
from .views import (
    AddProjectView, RetrieveProjectView, RetrieveProjectsView, UpdateProjectView,
    RemoveProjectStudyAreaView, DeleteProjectView, RestoreProjectView, 
    DeleteProjectPermanentlyView,
)

urlpatterns = [
    # PROJECT ROUTES
    path("project/add/", AddProjectView.as_view(), name="add-project"),
    path("project/get/<int:project_id>/", RetrieveProjectView.as_view(), name="retrieve-project"),
    path("project/get/", RetrieveProjectsView.as_view(), name="retrieve-projects"),
    path("project/update/<int:project_id>/", UpdateProjectView.as_view(), name="update-project"),
    path("project/study_area/remove/<int:study_area_id>/", RemoveProjectStudyAreaView.as_view(), name="remove-project-study-area"),
    path("project/delete/<int:project_id>/", DeleteProjectView.as_view(), name="delete-project"),
    path("project/restore/<int:project_id>/", RestoreProjectView.as_view(), name="restore-project"),
    path("project/delete/permanently/<int:project_id>/", DeleteProjectPermanentlyView.as_view(), name="delete-project-permanently"),
]