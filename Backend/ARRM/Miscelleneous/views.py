from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import AcademicYear, Semester
from .serializers import AcademicYearSerializer, SemesterSerializer
from Account.permissions import IsBlacklistedToken


class AddAcademicYearView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken, IsAdminUser]

    def post(self, request):
        serializer = AcademicYearSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            AcademicYear.mark_completed()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RetrieveAcademicYearsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]
    serializer_class = AcademicYearSerializer
    queryset = AcademicYear.objects.all()
    filterset_fields = ["start_year", "end_year", "is_completed"]

    def get_queryset(self):
        return AcademicYear.objects.filter()
    

class DeleteAcademicYearView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken, IsAdminUser]

    def delete(self, request, academic_year_id):
        try:
            academic_year = AcademicYear.objects.get(id=academic_year_id)
        except AcademicYear.DoesNotExist:
            return Response({"error": "Academic year not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if academic_year.user != request.user or not request.user.is_staff:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)

        academic_year.delete()
        return Response({"success": "Academic year deleted successfully"}, status=status.HTTP_200_OK)
    

class AddSemesterView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken, IsAdminUser]

    def post(self, request):
        serializer = SemesterSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            Semester.mark_completed()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveSemesterView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request, semester_id):
        try:
            semester = Semester.objects.get(id=semester_id)
        except Semester.DoesNotExist:
            return Response({"error": "Semester not found!"}, status=status.HTTP_404_NOT_FOUND)
                
        serializer = SemesterSerializer(semester, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RetrieveSemestersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()
    filterset_fields = ["academic_year", "semester", "is_completed"]

    def get_queryset(self):
        return Semester.objects.filter()
    

class DeleteSemesterView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken, IsAdminUser]

    def delete(self, request, semester_id):
        try:
            semester = Semester.objects.get(id=semester_id)
        except Semester.DoesNotExist:
            return Response({"error": "Semester not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if semester.user != request.user or not request.user.is_staff:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)

        semester.delete()
        return Response({"success": "Semester deleted successfully"}, status=status.HTTP_200_OK)