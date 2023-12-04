from re import S
from urllib import response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from Backend.ARRM.Profile.models import StudyArea

from .models import Project, ProjectStudyArea
from .serializers import ProjectSerializer
from Account.permissions import IsBlacklistedToken


class AddProjectView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def post(self, request):
        serializer = ProjectSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RetrieveProjectView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProjectSerializer(project)
        response = serializer.to_representation(project)
        return Response(response, status=status.HTTP_200_OK)
    

class RetrieveProjectsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    filterset_fields = ["title", "status", "visibility", "created_at"]
    
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)
    

class UpdateProjectView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def put(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProjectSerializer(project, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            response = serializer.to_representation(project)
            return Response(response, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RemoveProjectStudyAreaView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request):
        project_id = request.data.get("project_id")
        study_area = request.data.get("study_area")

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        if study_area not in StudyArea.values:
            return Response({"error": "Invalid study area!"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            project_study_area = ProjectStudyArea.objects.get(project=project, study_area=study_area)
        except ProjectStudyArea.DoesNotExist:
            return Response({"error": "Study area not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        project_study_area.delete()
        response = ProjectSerializer(project).to_representation(project)
        return Response(response, status=status.HTTP_200_OK)
    

class DeleteProjectView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def patch(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        # set is_deleted to True
        project.is_deleted = True # type: ignore
        project.save()
        return Response({"success": f"{project.title} has been moved to trash!"}, status=status.HTTP_200_OK)
    

class RestoreProjectView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def patch(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        # set is_deleted to False
        project.is_deleted = False # type: ignore
        project.save()
        return Response({"success": f"{project.title} restored from trash successfully!"}, status=status.HTTP_200_OK)
    

class DeleteProjectPermanentlyView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken, IsAdminUser]

    def delete(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if not project.is_deleted: # type: ignore
            return Response({"error": f"{project.title} is not in the trash!"}, status=status.HTTP_400_BAD_REQUEST)

        if project.user != request.user or not request.user.is_staff:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)

        project.delete()
        return Response({"success": "Project deleted permanently"}, status=status.HTTP_200_OK)