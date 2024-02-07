from turtle import st
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from datetime import timedelta
from django.utils import timezone

from .models import (
    Project, ProjectStatus, ProjectStudyArea, TeamMemberRole, ProjectRole, ProjectTeam, ProjectTeamRequest, 
    ProjectTeamInvitation, ProjectMatchScores, Milestone, ProjectMilestoneTemplate, ProjectMilestone, ProjectTask, 
    ProjectTaskAssignment, ProjectTaskFeedback, BlindProjectFeedback)
from .serializers import (
    ProjectSerializer, TeamMemberRoleSerializer, ProjectRoleSerializer, ProjectMatchScoresSerializer, ProjectTeamRequestSerializer, 
    ProjectTeamInvitationSerializer, MilestoneSerializer, ProjectMilestoneSerializer, ProjectTaskSerializer, ProjectTeamSerializer, 
    ProjectTaskFeedbackSerializer, BlindProjectFeedbackSerializer)
from .helper import (
    PROJECT_MILESTONE_TEMPLATE_DICT, TOTAL_MATCH_SCORE, compute_degree_match_score, compute_interest_match_score, 
    compute_project_study_area_match_score, get_cumulative_task_hours, get_milestone_dict, get_ra_available_hours, 
    get_available_ras, compute_faculty_study_area_match_score,)
from Account.permissions import IsBlacklistedToken
from Account.models import Role, UserAccount
from Profile.models import Notification, ResearchAssistant, StudyArea
from Profile.serializers import ResearchAssistantSerializer


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

            # add user as project team member
            # if the admin team member role does not exist, create it
            if not TeamMemberRole.objects.filter(name="Admin").exists():
                admin_role = TeamMemberRole(
                    name="Admin",
                    user=UserAccount.objects.filter(role=Role.ADMIN).first()
                )
                admin_role.save()
            else:
                admin_role = TeamMemberRole.objects.get(name="Admin")

            # create project role
            project_role = ProjectRole(
                project=project,
                team_member_role=admin_role
            )
            project_role.save()

            project_team = ProjectTeam(
                user=request.user,
                project_role=project_role
            )
            project_team.save()

            # create notification for project member addition
            notification = Notification(
                user=request.user,
                title="Project Membership!",
                message=f"You have been added as a member of the '{project.title}' project!",
            )
            notification.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RetrieveProjectView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id, is_deleted=False)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        # delete project matching scores older than 1 day
        ProjectMatchScores.clean_matches(project)
        
        serializer = ProjectSerializer(project, context={"request": request})
        response = serializer.to_representation(project)
        return Response(response, status=status.HTTP_200_OK)
    

class RetrieveProjectsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    filterset_fields = ["title", "status", "visibility", "created_at"]
    
    def get_queryset(self):
        projects = ProjectTeam.objects.filter(user=self.request.user)
        return Project.objects.filter(id__in=[project.project.id for project in projects], is_deleted=False)


class RetrievePublicProjectsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    filterset_fields = ["title", "status", "created_at"]
    
    def get_queryset(self):
        return Project.objects.filter(visibility="public", is_deleted=False)


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
            if not project.description or not project.start_date or not project.end_date or not project.estimated_project_hours:
                # create notification for failure
                notification = Notification(
                    user=request.user,
                    title="Project Visibility Update Failed!",
                    message=f"{project.title}'s visibility has not been updated to public. Project description, start date, end date and estimated weekly hours are required for public projects! Please update the project details and try again!", 
                )
                notification.save()
                return Response({"error": "Project description, start date, end date and estimated weekly hours are required for public projects!"}, 
                                status=status.HTTP_400_BAD_REQUEST)
        
        project.visibility = visibility
        project.save()

        # create notification for project visibility update
        notification = Notification(
            user=request.user,
            title="Project Visibility Updated!",
            message=f"{project.title}'s visibility has been updated to {visibility} successfully!", 
        )
        notification.save()
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
        project.is_deleted = True
        project.save()

        # create notification for project deletion
        notification = Notification(
            user=request.user,
            title="Project Deleted!",
            message=f"{project.title} has been moved to trash successfully! You can restore it from the trash if you deleted it by mistake!", 
        )
        notification.save()
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
        project.is_deleted = False
        project.save()
        return Response({"success": f"{project.title} has been restored from trash successfully!"}, status=status.HTTP_200_OK)
    

class DeleteProjectPermanentlyView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if not project.is_deleted:
            return Response({"error": f"{project.title} is not in the trash!"}, status=status.HTTP_400_BAD_REQUEST)
        if project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)

        project.delete()
        return Response({"success": "Project deleted permanently!"}, status=status.HTTP_200_OK)
    

class CreateTeamMemberRoleView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def post(self, request):
        if request.user.role != Role.FACULTY:
            return Response({"error": "You do not have permission to perform this action!"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = TeamMemberRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RetrieveTeamMemberRolesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request):
        default_roles = TeamMemberRole.objects.filter(name="Default")
        user_member_roles = TeamMemberRole.objects.filter(user=request.user)
        project_roles = default_roles.union(user_member_roles)
        return Response(TeamMemberRoleSerializer(project_roles, many=True).data, status=status.HTTP_200_OK)
    

class DeleteTeamMemberRoleView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request, role_id):
        try:
            team_member_role = TeamMemberRole.objects.get(id=role_id)
        except TeamMemberRole.DoesNotExist:
            return Response({"error": "Project role not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if team_member_role.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)

        team_member_role.delete()
        return Response({"success": "Project role deleted successfully!"}, status=status.HTTP_200_OK)
    

class AddRoleToProjectView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def post(self, request):
        try:
            project = Project.objects.get(id=request.data.get("project_id"))
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProjectRoleSerializer(context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        


class RemoveRoleFromProjectView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request):
        try:
            project = Project.objects.get(id=request.data.get("project_id"))
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            team_member_role = TeamMemberRole.objects.get(id=request.data.get("team_member_role_id"))
        except TeamMemberRole.DoesNotExist:
            return Response({"error": "Team member role not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if ProjectRole.objects.filter(project=project, team_member_role=team_member_role).exists():
            project_role = ProjectRole.objects.get(project=project, team_member_role=team_member_role)
            project_role.delete()
            return Response({"success": "Project role removed successfully!"}, status=status.HTTP_200_OK)
        
        return Response({"error": "Project role not found!"}, status=status.HTTP_404_NOT_FOUND)
    

class RetrieveProjectRolesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        project_roles = ProjectRole.objects.filter(project=project)
        return Response(ProjectRoleSerializer(project_roles, many=True).data, status=status.HTTP_200_OK)
    

class RequestProjectMembershipView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def post(self, request, project_role_id):
    
        if request.user.role == Role.ADMIN:
            return Response({"error": "You cannot request membership as admin!"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            project_role = ProjectRole.objects.get(id=project_role_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if ProjectTeam.objects.filter(project_role=project_role, user=request.user).exists():
            return Response({"error": f"You are already a member of the '{project_role.project.title}' project!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if ProjectTeamRequest.objects.filter(project_role=project_role, user=request.user).exists():
            return Response({"error": f"You have already requested membership for the '{project_role.project.title}' project!"}, status=status.HTTP_400_BAD_REQUEST)
        
        project_team_request = ProjectTeamRequest(
            project_role=project_role,
            user=request.user
        )
        project_team_request.save()

        # create notification for request
        notification = Notification(
            user=project_role.project.user,
            title="Project Membership Request!",
            message=f"{request.user.email} has requested to join the '{project_role.project.title}' project as a {project_role.name}!", 
        )
        notification.save()
        return Response({"success": "Project membership request sent successfully!"}, status=status.HTTP_201_CREATED)


class RetrieveProjectMembershipRequestsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        project_team_requests = ProjectTeamRequest.objects.filter(project_role__project=project)
        return Response(ProjectTeamRequestSerializer(project_team_requests, many=True).data, status=status.HTTP_200_OK)


class AcceptProjectMembershipView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def post(self, request, project_request_id):
        try:
            project_team_request = ProjectTeamRequest.objects.get(id=project_request_id)
        except ProjectTeamRequest.DoesNotExist:
            return Response({"error": "Project membership request not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project_team_request.project_role.project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        if ProjectTeam.objects.filter(project_role=project_team_request.project_role, user=project_team_request.user).exists():
            return Response({"error": f"{project_team_request.user.email} is already a member of the '{project_team_request.project_role.project.title}' project!"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        project_team = ProjectTeam(
            project_role=project_team_request.project_role,
            user=project_team_request.user
        )
        project_team.save()
        project_team_request.delete()

        # create notification for acceptance
        notification = Notification(
            user=project_team_request.user,
            title="Project Membership Request Accepted!",
            message=f"Your request to join the '{project_team_request.project_role.project.title}' project as a {project_team_request.project_role.name} has been accepted!", 
        )
        notification.save()
        return Response({"success": f"{project_team.user.email} is now a member of the '{project_team.project_role.project.title}' project!"}, 
                        status=status.HTTP_200_OK)


class RejectProjectMembershipView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request, project_request_id):
        try:
            project_team_request = ProjectTeamRequest.objects.get(id=project_request_id)
        except ProjectTeamRequest.DoesNotExist:
            return Response({"error": "Project membership request not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project_team_request.project_role.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        project_team_request.delete()

        # create notification for rejection
        notification = Notification(
            user=project_team_request.user,
            title="Project Membership Request Rejected!",
            message=f"Your request to join the '{project_team_request.project_role.project.title}' project as a {project_team_request.project_role.name} has been rejected!", 
        )
        notification.save()
        return Response({"success": "Project membership request rejected successfully!"}, status=status.HTTP_200_OK)


class DeleteProjectMembershipRequestView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request, project_request_id):
        try:
            project_team_request = ProjectTeamRequest.objects.get(id=project_request_id)
        except ProjectTeamRequest.DoesNotExist:
            return Response({"error": "Project membership request not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project_team_request.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        project_team_request.delete()
        return Response({"success": "Project membership request deleted successfully!"}, status=status.HTTP_200_OK)


class InviteResearchAssistantView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def post(self, request):
        project_role_id = request.data.get("project_role_id")
        user_id = request.data.get("user_id")

        try:
            project_role = ProjectRole.objects.get(id=project_role_id)
        except Project.DoesNotExist:
            return Response({"error": "Project role not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project_role.project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = UserAccount.objects.get(id=user_id)
        except UserAccount.DoesNotExist:
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if ProjectTeam.objects.filter(project_role=project_role, user=user).exists():
            return Response({"error": f"{user.email} is already a member of the '{project_role.project.title}' project!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if ProjectTeamInvitation.objects.filter(project_role=project_role, user=user).exists():
            return Response({"error": f"{user.email} has already been invited to the '{project_role.project.title}' project!"}, status=status.HTTP_400_BAD_REQUEST)
        
        project_team_invitation = ProjectTeamInvitation(
            project_role=project_role,
            user=user
        )
        project_team_invitation.save()
        return Response({"success": f"{user.email} has been invited to the '{project_role.project.title}' project!"}, status=status.HTTP_201_CREATED)


class RetrieveProjectInvitationsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)

        project_team_invitations = ProjectTeamInvitation.objects.filter(project_role__project=project)
        return Response(ProjectTeamInvitationSerializer(project_team_invitations, many=True).data, status=status.HTTP_200_OK)


class AcceptProjectInvitationView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def post(self, request, project_invite_id):
        try:
            project_team_invitation = ProjectTeamInvitation.objects.get(id=project_invite_id)
        except ProjectTeamInvitation.DoesNotExist:
            return Response({"error": "Project invitation not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project_team_invitation.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        if ProjectTeam.objects.filter(project_role=project_team_invitation.project_role, user=project_team_invitation.user).exists():
            return Response({"error": f"You are already a member of the '{project_team_invitation.project_role.project.title}' project!"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        project_team = ProjectTeam(
            project_role=project_team_invitation.project_role,
            user=project_team_invitation.user
        )
        project_team.save()
        project_team_invitation.delete()
        return Response({"success": f"You are now a member of the '{project_team.project_role.project.title}' project!"}, 
                        status=status.HTTP_200_OK)


class DeclineProjectInvitationView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request, project_invite_id):
        try:
            project_team_invitation = ProjectTeamInvitation.objects.get(id=project_invite_id)
        except ProjectTeamInvitation.DoesNotExist:
            return Response({"error": "Project invitation not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project_team_invitation.project_role.project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        project_team_invitation.delete()
        return Response({"success": "Project invitation rejected successfully!"}, status=status.HTTP_200_OK)


class DeleteProjectInvitationView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request, project_invite_id):
        try:
            project_team_invitation = ProjectTeamInvitation.objects.get(id=project_invite_id)
        except ProjectTeamInvitation.DoesNotExist:
            return Response({"error": "Project invitation not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project_team_invitation.project_role.project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        project_team_invitation.delete()
        return Response({"success": "Project invitation deleted successfully!"}, status=status.HTTP_200_OK)


class RetrieveProjectTeamMembersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)

        if not ProjectTeam.objects.filter(project_role__project=project, user=request.user).exists():
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)

        project_team_members = ProjectTeam.objects.filter(project_role__project=project)
        return Response(ProjectTeamSerializer(project_team_members, many=True).data, status=status.HTTP_200_OK)


class RemoveProjectTeamMemberView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request, project_member_id):
        try:
            project_team_member = ProjectTeam.objects.get(id=project_member_id)
        except ProjectTeam.DoesNotExist:
            return Response({"error": "Project team member not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project_team_member.project_role.project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        if project_team_member.user == request.user:
            return Response({"error": "You cannot remove yourself from the project!"}, status=status.HTTP_400_BAD_REQUEST)
        
        project_team_member.delete()
        return Response({"success": "Project team member removed successfully!"}, status=status.HTTP_200_OK)
    

class ProjectMatchScoresView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def post(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        # delete existing project matching scores before computing new ones
        ProjectMatchScores.objects.filter(project=project).delete()
        
        # ensure the project details are complete
        if not project.description or not project.start_date or not project.end_date:
            return Response({"error": "Project details are not complete. Project description, start date and end date are required to complete project!"}, status=status.HTTP_400_BAD_REQUEST)

        # ensure project has study areas
        if not ProjectStudyArea.objects.filter(project=project).exists():
            return Response({"error": "Project has no study areas! Study areas are required for matching!"}, status=status.HTTP_400_BAD_REQUEST)

        # ensure estimated weekly hours is not None
        if not project.estimated_project_hours:
            return Response({"error": "Estimated project hours is required for matching!"}, status=status.HTTP_400_BAD_REQUEST)
        
        # retrieve all project tasks and compute required project hours
        assigned_project_hours = get_cumulative_task_hours(project)

        # retrieve RAs and compute available hours
        ra_available_hours = get_ra_available_hours()
        available_ras = get_available_ras(ra_available_hours, project, assigned_project_hours)

        # retrieve project study areas
        project_study_areas = ProjectStudyArea.objects.filter(project=project)
        project_study_areas = [project_study_area.study_area for project_study_area in project_study_areas]
        
        # retrieve RA profile, interests, study areas, degrees, and compute matching scores
        ra_matching_scores = dict()
        for ra_id in available_ras:
            ra = ResearchAssistantSerializer(ResearchAssistant.objects.get(user__id=ra_id), context={"request": request}).data
            matching_score = 0  # (OUT OF 7)

            # compute project study area matching score (OUT OF 3)
            matching_score += compute_project_study_area_match_score(ra, project_study_areas)

            # compute faculty study area matching score (OUT OF 2)
            matching_score += compute_faculty_study_area_match_score(ra, project.user)
            
            # compute interest to project title & description matching score (OUT OF 1)
            matching_score += compute_interest_match_score(ra, project)

            # compute RA and Faculty degree matching score (OUT OF 1)
            matching_score += compute_degree_match_score(ra, project)           

            ra_matching_scores[ra_id] = matching_score

        # order the dictionary in descending order based on the 
        # matching scores and store the first five
        ra_matching_scores = dict(sorted(ra_matching_scores.items(), key=lambda item: item[1], reverse=True)[:5])
        
        for ra_id, matching_score in ra_matching_scores.items():
            project_match_score = ProjectMatchScores(
                project=project,
                user=UserAccount.objects.get(id=ra_id),
                score=(matching_score / TOTAL_MATCH_SCORE) * 100
            )
            project_match_score.save()
        
        return Response(ProjectMatchScoresSerializer(ProjectMatchScores.objects.filter(project=project), many=True).data, status=status.HTTP_200_OK)


class RetrieveProjectMatchScoresView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)

        if project.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        return Response(ProjectMatchScoresSerializer(ProjectMatchScores.objects.filter(project=project), many=True).data, status=status.HTTP_200_OK)


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
            project_milestone = AddProjectTaskView.create_project_milestone(project, milestone)
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
            MILESTONE_DICT = get_milestone_dict()
            if milestone in MILESTONE_DICT.keys():
                milestone = Milestone.objects.get(name=MILESTONE_DICT[milestone])
            else:
                milestone = Milestone.objects.create(name=milestone)
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


class RetrieveTaskView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request, task_id):
        try:
            project_task = ProjectTask.objects.get(id=task_id)
        except ProjectTask.DoesNotExist:
            return Response({"error": "Project task not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProjectTaskSerializer(project_task, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveTasksView(generics.ListAPIView):
    # should allow to filter by status, due date, project milestone
    permission_classes = [IsAuthenticated, IsBlacklistedToken]
    serializer_class = ProjectTaskSerializer
    queryset = ProjectTask.objects.all()
    filterset_fields = ["name", "status", "due_date", "project_milestone", "project_milestone__name"]

    def get_queryset(self):
        # retrieve tasks for all project the user is a part of, use ProjectTeam to decide this
        project_tasks = ProjectTaskAssignment.objects.filter(user=self.request.user)

        # pre-fetch project_milestone for each task, ensure that the task has been assigned to the user
        queryset = ProjectTask.objects.filter(
            project_milestone__project__in=[assigned_task.project_task.project_milestone.project for assigned_task in project_tasks]
        ).prefetch_related("project_milestone")

        return queryset


class UpdateTaskView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def patch(self, request, task_id):
        try:
            project_task = ProjectTask.objects.get(id=task_id)
        except ProjectTask.DoesNotExist:
            return Response({"error": "Project task not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != project_task.project_milestone.project.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProjectTaskSerializer(project_task, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():  
            serializer.save()
            response = serializer.to_representation(project_task)
            return Response(response, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AssignTaskView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def post(self, request):
        if "task_id" not in request.data.keys():
            return Response({"error": "Task ID is required!"}, status=status.HTTP_400_BAD_REQUEST)
        
        task_id = request.data["task_id"]

        try:
            project_task = ProjectTask.objects.get(id=task_id)
        except ProjectTask.DoesNotExist:
            return Response({"error": "Project task not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != project_task.project_milestone.project.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        if project_task.status == ProjectStatus.DONE:
            return Response({"error": "You cannot assign a completed task!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if "assignee" not in request.data.keys():
            return Response({"error": "Assignee is required!"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            assignee = UserAccount.objects.get(id=request.data["assignee"])
        except UserAccount.DoesNotExist:
            return Response({"error": "Assignee not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if not ProjectTeam.objects.filter(project_role__project=project_task.project_milestone.project, user=assignee).exists():
            return Response({"error": "Assignee is not a member of the project!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if ProjectTaskAssignment.objects.filter(project_task=project_task, user=assignee).exists():
            return Response({"error": "Assignee has already been assigned to this task!"}, status=status.HTTP_400_BAD_REQUEST)
        
        project_task_assignment = ProjectTaskAssignment(
            project_task=project_task,
            user=assignee
        )

        project_task_assignment.save()
        serializer = ProjectTaskSerializer(project_task, context={"request": request})
        response = serializer.to_representation(project_task)
        return Response(response, status=status.HTTP_201_CREATED)
    

class UnassignTaskView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request, task_id):
        if "task_id" not in request.data.keys():
            return Response({"error": "Task ID is required!"}, status=status.HTTP_400_BAD_REQUEST)
        
        task_id = request.data["task_id"]

        try:
            project_task = ProjectTask.objects.get(id=task_id)
        except ProjectTask.DoesNotExist:
            return Response({"error": "Project task not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != project_task.project_milestone.project.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        if project_task.status == ProjectStatus.DONE:
            return Response({"error": "You cannot unassign a completed task!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if "assignee" not in request.data.keys():
            return Response({"error": "Assignee is required!"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            assignee = UserAccount.objects.get(id=request.data["assignee"])
        except UserAccount.DoesNotExist:
            return Response({"error": "Assignee not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if not ProjectTeam.objects.filter(project_role__project=project_task.project_milestone.project, user=assignee).exists():
            return Response({"error": "Assignee is not a member of the project!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not ProjectTaskAssignment.objects.filter(project_task=project_task, user=assignee).exists():
            return Response({"error": "Assignee has not been assigned to this task!"}, status=status.HTTP_400_BAD_REQUEST)
        
        project_task_assignment = ProjectTaskAssignment.objects.get(project_task=project_task, user=assignee)
        project_task_assignment.delete()
        serializer = ProjectTaskSerializer(project_task, context={"request": request})
        response = serializer.to_representation(project_task)
        return Response(response, status=status.HTTP_200_OK)


class DeleteProjectTaskView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request, task_id):
        try:
            project_task = ProjectTask.objects.get(id=task_id)
        except ProjectTask.DoesNotExist:
            return Response({"error": "Project task not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != project_task.project_milestone.project.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        if project_task.status == ProjectStatus.DONE:
            return Response({"error": "You cannot delete a completed task!"}, status=status.HTTP_400_BAD_REQUEST)
        
        project_task.delete()
        return Response({"success": "Project task deleted successfully!"}, status=status.HTTP_200_OK)
    

class GiveProjectTaskFeedbackView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def post(self, request):
        serializer = ProjectTaskFeedbackSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            project_task = ProjectTask.objects.get(id=request.data["project_task"])
            task_serializer =  ProjectTaskSerializer(project_task, context={"request": request})
            return Response(task_serializer.to_representation(project_task), status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RetrieveProjectTaskFeedbacksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request, task_id):
        try:
            project_task = ProjectTask.objects.get(id=task_id)
        except ProjectTask.DoesNotExist:
            return Response({"error": "Project task not found!"}, status=status.HTTP_404_NOT_FOUND)
        team_members = ProjectTeam.objects.filter(project_role__project=project_task.project_milestone.project)
        for team_member in team_members:
            print(team_member.user.email)
        
        if not ProjectTeam.objects.filter(project_role__project=project_task.project_milestone.project, user=request.user).exists():
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        project_task_feedbacks = ProjectTaskFeedback.objects.filter(project_task=project_task)
        return Response(ProjectTaskFeedbackSerializer(project_task_feedbacks, many=True).data, status=status.HTTP_200_OK)
    

class UpdateProjectTaskFeedbackView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def patch(self, request, feedback_id):
        try:
            task_feedback = ProjectTaskFeedback.objects.get(id=feedback_id)
        except ProjectTaskFeedback.DoesNotExist:
            return Response({"error": "Project task feedback not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != task_feedback.reviewer:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        # ensure feedback cannot be changed if its past 15 minutes
        if task_feedback.created_at < timezone.now() - timedelta(minutes=15):
            return Response({"error": "You cannot change feedback that is more than 15 minutes old!"}, status=status.HTTP_400_BAD_REQUEST)
        
        task_feedback.feedback = request.data["feedback"]
        task_feedback.edited = True
        task_feedback.save()
        project_task = ProjectTask.objects.get(id=task_feedback.project_task.id)
        task_serializer =  ProjectTaskSerializer(project_task, context={"request": request})
        return Response(task_serializer.to_representation(project_task), status=status.HTTP_200_OK)
    

class GiveBlindFeedbackView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def post(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project.status != ProjectStatus.DONE:
            return Response({"error": "You cannot give feedback for a project that has not been completed!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not ProjectTeam.objects.filter(project_role__project=project, user=request.user).exists():
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        if BlindProjectFeedback.objects.filter(reviewer=request.user, project=project).exists():
            return Response({"error": "You have already given feedback for this project!"}, status=status.HTTP_400_BAD_REQUEST)
        
        # ensure RAs can only give feedback to the project owner
        if request.user.role == Role.RA and project.user.id != request.data["intended_user"]:
            return Response({"error": "You can only give feedback to the project owner!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # ensure intended_user is a project member
            if not ProjectTeam.objects.filter(project_role__project=project, user__id=request.data["intended_user"]).exists():
                return Response({"error": "The intended user is not a member of the project!"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BlindProjectFeedbackSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RetrieveBlindFeedbacksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != project.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        blind_feedbacks = BlindProjectFeedback.objects.filter(project=project)
        return Response(BlindProjectFeedbackSerializer(blind_feedbacks, many=True).data, status=status.HTTP_200_OK)