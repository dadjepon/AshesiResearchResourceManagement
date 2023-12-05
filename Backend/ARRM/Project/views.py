from ast import Add
from re import A
import re
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import (Project, ProjectStatus, ProjectStudyArea, Milestone, ProjectMilestoneTemplate, 
                     ProjectMilestone, ProjectTask)
from .serializers import (ProjectSerializer, MilestoneSerializer, ProjectMilestoneSerializer, 
                          ProjectTaskSerializer)
from .helper import MILESTONE_DICT, PROJECT_MILESTONE_TEMPLATE_DICT
from Account.permissions import IsBlacklistedToken
from Account.models import Role
from Profile.models import StudyArea


class AddProjectView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def post(self, request):
        if request.user.role != Role.FACULTY:
            return Response({"error": "You do not have permission to perform this action!"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProjectSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            project = serializer.save()

            if "study_areas" in request.data.keys():
                for study_area in request.data["study_areas"]:                    
                    if study_area in StudyArea.values:              
                        if not ProjectStudyArea.objects.filter(project=project, study_area=study_area).exists():
                            project_study_area = ProjectStudyArea(
                                project=project,
                                study_area=study_area
                            )
                            project_study_area.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RetrieveProjectView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id, is_deleted=False)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProjectSerializer(project, context={"request": request})
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

    def patch(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProjectSerializer(project, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            if "study_areas" in request.data.keys():
                for study_area in request.data["study_areas"]:      
                    if study_area in StudyArea.values:              
                        if not ProjectStudyArea.objects.filter(project=project, study_area=study_area).exists():
                            project_study_area = ProjectStudyArea(
                                project=project,
                                study_area=study_area
                            )
                            project_study_area.save()
                    
            serializer.save()
            response = serializer.to_representation(project)
            return Response(response, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ChangeProjectVisibilityView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def patch(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        visibility = request.data.get("visibility")
        if visibility not in ["public", "private"]:
            return Response({"error": "Invalid visibility!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if visibility == "public":
            if not project.description or not project.start_date or not project.end_date:
                return Response({"error": "Project description, start date and end date are required for public projects!"}, status=status.HTTP_400_BAD_REQUEST)
        
        project.visibility = visibility
        project.save()
        response = ProjectSerializer(project, context={"request": request}).to_representation(project)
        return Response(response, status=status.HTTP_200_OK)
    

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
        response = ProjectSerializer(project, context={"request": request}).to_representation(project)
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
        return Response({"success": f"{project.title} has been restored from trash successfully!"}, status=status.HTTP_200_OK)
    

class DeleteProjectPermanentlyView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if not project.is_deleted: # type: ignore
            return Response({"error": f"{project.title} is not in the trash!"}, status=status.HTTP_400_BAD_REQUEST)
        print(request.user == project.user, request.user.is_staff)
        if project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)

        project.delete()
        return Response({"success": "Project deleted permanently"}, status=status.HTTP_200_OK)
    

class AddMilestoneView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken, IsAdminUser]

    def post(self, request):
        serializer = MilestoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RetrieveMilestoneView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request, milestone_id):
        try:
            milestone = Milestone.objects.get(id=milestone_id)
        except Milestone.DoesNotExist:
            return Response({"error": "Milestone not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MilestoneSerializer(milestone)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RetrieveMilestonesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]
    serializer_class = MilestoneSerializer
    queryset = Milestone.objects.all()
    filterset_fields = ["name"]
    
    def get_queryset(self):
        return Milestone.objects.filter()
    

class DeleteMilestoneView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken, IsAdminUser]

    def delete(self, request, milestone_id):
        try:
            milestone = Milestone.objects.get(id=milestone_id)
        except Milestone.DoesNotExist:
            return Response({"error": "Milestone not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        milestone.delete()
        return Response({"success": "Milestone deleted successfully!"}, status=status.HTTP_200_OK)
    

class AddProjectTaskView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def post(self, request, project_id):
        if request.user.role != Role.FACULTY:
            return Response({"error": "You do not have permission to perform this action!"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)

        if "template" in request.data:
            tasks_dict = AddProjectTaskView.get_tasks_dict_from_template(project, request)
        elif "tasks" in request.data:
            tasks_dict = request.data["tasks"]
        else:
            return Response({"error": "Invalid request!"}, status=status.HTTP_400_BAD_REQUEST)

        for milestone, tasks in tasks_dict.items():
            # create project milestone
            project_milestone = AddProjectTaskView.create_project_milestone(project, MILESTONE_DICT[milestone])
            if project_milestone is not None:
                # create project tasks
                for task in tasks:
                    AddProjectTaskView.create_project_task(project_milestone, task)
        
        representation = ProjectSerializer(project, context={"request": request}).to_representation(project)
        return Response(representation, status=status.HTTP_201_CREATED)
    
    @staticmethod
    def get_tasks_dict_from_template(project, request):
        # ensure no task has been added to the project, this is possible since 
        # a milestone will only exist if there is at least 1 task for it [SCRATCHED]
        
        # if ProjectMilestone.objects.filter(project=project).exists():
        #     return Response({"error": "You cannot add a template to a project that has tasks!"}, status=status.HTTP_400_BAD_REQUEST)
        
        # create the project tasks based on the template
        template = request.data["template"]
        tasks_dict = AddProjectTaskView.get_tasks_dict(template)
        return tasks_dict

    @staticmethod
    def get_tasks_dict(template):            
        if len(template) == 1 and template[0] == ProjectMilestoneTemplate.STANDARD:
            tasks_dict = PROJECT_MILESTONE_TEMPLATE_DICT
        else:
            tasks_dict = dict()
            for key in template:
                if key in ProjectMilestoneTemplate.values:
                    tasks_dict[key] = PROJECT_MILESTONE_TEMPLATE_DICT[key]

        return tasks_dict
    
    @staticmethod
    def create_project_milestone(project, milestone):
        try:
            milestone = Milestone.objects.get(name=milestone)
        except Milestone.DoesNotExist:
            return None

        if not ProjectMilestone.objects.filter(project=project, milestone=milestone).exists():

            project_milestone = ProjectMilestone(
                project=project,
                milestone=milestone
            )
            project_milestone.save()
            return project_milestone

        return ProjectMilestone.objects.get(project=project, milestone=milestone)
    
    @staticmethod
    def create_project_task(project_milestone, task):
        if not ProjectTask.objects.filter(project_milestone=project_milestone, name=task).exists():
            project_task = ProjectTask(
                project_milestone=project_milestone,
                name=task
            )
            project_task.save()


class RetrieveProjectMilestoneView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request, project_milestone_id):
        try:
            project_milestone = ProjectMilestone.objects.get(id=project_milestone_id)
        except ProjectMilestone.DoesNotExist:
            return Response({"error": "Project milestone not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProjectMilestoneSerializer(project_milestone, context={"request": request})
        response = serializer.to_representation(project_milestone)
        return Response(response, status=status.HTTP_200_OK)
    

class RemoveProjectTaskFromMilestoneView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request):
        task_id = request.data.get("task_id")
        milestone_id = request.data.get("milestone_id")

        try:
            project_milestone = ProjectMilestone.objects.get(id=milestone_id)
        except ProjectMilestone.DoesNotExist:
            return Response({"error": "Project milestone not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project_milestone.project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            project_task = ProjectTask.objects.get(id=task_id)
        except ProjectTask.DoesNotExist:
            return Response({"error": "Project task not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project_task.project_milestone != project_milestone:
            return Response({"error": "Project task does not belong to this milestone!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if project_task.status == ProjectStatus.DONE:
            return Response({"error": "You cannot remove a completed task!"}, status=status.HTTP_400_BAD_REQUEST)
        
        project_task.delete()
        response = ProjectMilestoneSerializer(project_milestone, context={"request": request}).to_representation(project_milestone)
        return Response(response, status=status.HTTP_200_OK)


class DeleteProjectMilestoneView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request, project_milestone_id):
        try:
            project_milestone = ProjectMilestone.objects.get(id=project_milestone_id)
        except ProjectMilestone.DoesNotExist:
            return Response({"error": "Project milestone not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != project_milestone.project.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        # don't allow delete if there are completed tasks under the milestone
        if ProjectTask.objects.filter(project_milestone=project_milestone, status=ProjectStatus.DONE).exists():
            return Response({"error": "You cannot delete a milestone that has completed tasks!"}, status=status.HTTP_400_BAD_REQUEST)
        
        project_milestone.delete()
        return Response({"success": "Project milestone deleted successfully!"}, status=status.HTTP_200_OK)