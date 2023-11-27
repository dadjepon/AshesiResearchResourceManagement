from os import urandom
from django.urls import path

from .views import (
    AddAcademicYearView, RetrieveAcademicYearsView, DeleteAcademicYearView,

    AddSemesterView, RetrieveSemesterView, RetrieveSemestersView, DeleteSemesterView,
)

urlpatterns = [
    # ACADEMIC YEAR ROUTES
    path("academic_year/add/", AddAcademicYearView.as_view(), name="add-academic-year"),
    path("academic_year/get/", RetrieveAcademicYearsView.as_view(), name="retrieve-academic-years"),
    path("academic_year/delete/<int:academic_year_id>/", DeleteAcademicYearView.as_view(), name="delete-academic-year"),

    # SEMESTER ROUTES
    path("semester/add/", AddSemesterView.as_view(), name="add-semester"),
    path("semester/get/<int:semester_id>/", RetrieveSemesterView.as_view(), name="retrieve-semester"),
    path("semester/get/", RetrieveSemestersView.as_view(), name="retrieve-semesters"),
    path("semester/delete/<int:semester_id>/", DeleteSemesterView.as_view(), name="delete-semester"),
]