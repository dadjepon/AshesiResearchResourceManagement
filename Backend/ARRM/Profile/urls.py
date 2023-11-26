from django.urls import path
from .views import (AddDegreeView, RetrieveDegreeView, RetrieveDegreesView, UpdateDegreeView, 
                    DeleteDegreeView, RestoreDegreeView, DeleteDegreePermanentlyView)

urlpatterns = [
    path("degree/add/", AddDegreeView.as_view(), name="add-degree"),
    path("degree/get/<int:degree_id>/", RetrieveDegreeView.as_view(), name="retrieve-degree"),
    path("degree/get/", RetrieveDegreesView.as_view(), name="retrieve-degrees"),
    path("degree/update/<int:degree_id>/", UpdateDegreeView.as_view(), name="update-degree"),
    path("degree/delete/<int:degree_id>/", DeleteDegreeView.as_view(), name="delete-degree"),
    path("degree/restore/<int:degree_id>/", RestoreDegreeView.as_view(), name="restore-degree"),
    path("degree/delete/permanently/<int:degree_id>/", DeleteDegreePermanentlyView.as_view(), name="delete-degree-permanently"),
]