from django.urls import path
from .views import (
    AddDegreeView, RetrieveDegreeView, RetrieveDegreesView, UpdateDegreeView, 
    VerifyDegreeView, DeleteDegreeView, RestoreDegreeView, DeleteDegreePermanentlyView,

    AddWritingSampleView, RetrieveWritingSampleView, RetrieveWritingSamplesView, 
    UpdateWritingSampleView, DeleteWritingSampleView,

    AddInterestView, RetrieveInterestsView, DeleteInterestView,

    CreateResearchAssistantView, RetrieveResearchAssistantView, UpdateResearchAssistantView,

    CreateFacultyView, RetrieveFacultyView, UpdateFacultyView,
)

urlpatterns = [
    # DEGREE ROUTES
    path("degree/add/", AddDegreeView.as_view(), name="add-degree"),
    path("degree/get/<int:degree_id>/", RetrieveDegreeView.as_view(), name="retrieve-degree"),
    path("degree/get/", RetrieveDegreesView.as_view(), name="retrieve-degrees"),
    path("degree/update/<int:degree_id>/", UpdateDegreeView.as_view(), name="update-degree"),
    path("degree/verify/<int:degree_id>/", VerifyDegreeView.as_view(), name="verify-degree"),
    path("degree/delete/<int:degree_id>/", DeleteDegreeView.as_view(), name="delete-degree"),
    path("degree/restore/<int:degree_id>/", RestoreDegreeView.as_view(), name="restore-degree"),
    path("degree/delete/permanently/<int:degree_id>/", DeleteDegreePermanentlyView.as_view(), 
         name="delete-degree-permanently"),

    # WRITING SAMPLE ROUTES
    path("sample/add/", AddWritingSampleView.as_view(), name="add-sample"),
    path("sample/get/<int:sample_id>/", RetrieveWritingSampleView.as_view(), name="retrieve-sample"),
    path("sample/get/", RetrieveWritingSamplesView.as_view(), name="retrieve-samples"),
    path("sample/update/<int:sample_id>/", UpdateWritingSampleView.as_view(), name="update-sample"),
    path("sample/delete/<int:sample_id>/", DeleteWritingSampleView.as_view(), name="delete-sample"),

    # INTEREST ROUTES
    path("interest/add/", AddInterestView.as_view(), name="add-interest"),
    path("interest/get/", RetrieveInterestsView.as_view(), name="retrieve-interests"),
    path("interest/delete/<int:interest_id>/", DeleteInterestView.as_view(), name="delete-interest"),

    # RESEARCH ASSISTANT ROUTES
    path("ra/create/", CreateResearchAssistantView.as_view(), name="create-research-assistant"),
    path("ra/get/", RetrieveResearchAssistantView.as_view(), name="retrieve-research-assistant"),
    path("ra/update/", UpdateResearchAssistantView.as_view(), name="update-research-assistant"),

    # FACULTY ROUTES
    path("faculty/create/", CreateFacultyView.as_view(), name="create-faculty"),
    path("faculty/get/", RetrieveFacultyView.as_view(), name="retrieve-faculty"),
    path("faculty/update/", UpdateFacultyView.as_view(), name="update-faculty"),
]