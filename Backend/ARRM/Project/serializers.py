from asyncio import tasks
import re
from rest_framework import serializers
from datetime import datetime, timedelta

from .models import (
    ProjectStatus, Project, ProjectStudyArea, ProjectTeam, ProjectTeamRequest,
    ProjectTeamInvitation, ProjectMatchScores, Milestone, ProjectMilestone, ProjectTask, ProjectTaskFeedback,
)
from Profile.models import StudyArea
from Account.models import Role, UserAccount


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = Project
        fields = [
            "id", "user", "title", "description", "status", "start_date", 
            "end_date", "visibility", "estimated_project_hours", "is_deleted", "created_at"
        ]
        
    def get_user(self, obj):
        return self.context["request"].user.email
    
    def validate_title(self, value):
        if len(value) > 100:
            raise serializers.ValidationError("Title must not exceed 500 characters!")
        
        return value
    
    def validate_status(self, value):
        if value not in ProjectStatus.values:
            raise serializers.ValidationError("Invalid project status!")
        
        if value == ProjectStatus.COMPLETED:
            return ProjectStatus.IN_PROGRESS
        
        return value
    
    def validate_visibility(self, value):
        if value not in ["public", "private"]:
            raise serializers.ValidationError("Invalid visibility!")
        
        return value
    
    def validate(self, attrs):
        # ensure visibility is private if project description, 
        # start date and end date are not provided

        if not "description" in attrs.keys() or not "start_date" in attrs.keys() or not "end_date" in attrs.keys() or not "estimated_project_hours" in attrs.keys():
            attrs["visibility"] = "private"

        if "end_date" in attrs.keys() and "start_date" in attrs.keys():
            if attrs["end_date"] < attrs["start_date"]:
                raise serializers.ValidationError("End date must be greater than start date!")

        attrs["user"] = self.context["request"].user
        return attrs
    
    def create(self, validated_data):
        project = super().create(validated_data)        
        project.save()
        
        if "study_areas" in validated_data.keys():
            for study_area in validated_data["study_areas"]:
                project_study_area = ProjectStudyArea(
                    project=project,
                    study_area=study_area
                )
                project_study_area.save()
        
        return project
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        
        if "study_areas" in validated_data.keys():
            project_study_areas = ProjectStudyArea.objects.filter(project=instance)
            project_study_areas.delete()
            
            for study_area in validated_data["study_areas"]:
                project_study_area = ProjectStudyArea(
                    project=instance,
                    study_area=study_area
                )
                project_study_area.save()
        
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = instance.user.email

        # retrieve study areas
        representation["study_areas"] = []
        project_study_areas = ProjectStudyArea.objects.filter(project=instance)
        for project_study_area in project_study_areas:
            representation["study_areas"].append(project_study_area.study_area)

        # retrieve milestones
        representation["milestones"] = []
        for project_milestone in ProjectMilestone.objects.filter(project=instance):
            milestone = ProjectMilestoneSerializer(project_milestone, context={"request": self.context["request"]})
            representation["milestones"].append(milestone.to_representation(project_milestone))

        return representation
    

class ProjectTeamSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField("get_project")
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = ProjectTeam
        fields = ["id", "project", "user"]

    def get_project(self, obj):
        return obj.project.title
    
    def get_user(self, obj):
        return obj.user.email


class ProjectTeamRequestSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField("get_project")
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = ProjectTeamRequest
        fields = ["id", "project", "user"]

    def get_project(self, obj):
        return obj.project.title
    
    def get_user(self, obj):
        return obj.user.email


class ProjectTeamInvitationSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField("get_project")
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = ProjectTeamInvitation
        fields = ["id", "project", "user"]
 
    def get_project(self, obj):
        return obj.project.title
    
    def get_user(self, obj):
        return obj.user.email
    

class ProjectMatchScoresSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProjectMatchScores
        fields = ["id", "project", "user", "score", "created_at"]

    def validate_project(self, value):
        if not Project.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Invalid project!")
        
        return value
    
    def validate_user(self, value):
        if not UserAccount.objects.filter(id=value.id, role=Role.RA).exists():
            raise serializers.ValidationError("Invalid user!")
        
        return value
    
    def validate_score(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Invalid score!")
        
        return value
    
    def validate(self, attrs):
        if ProjectMatchScores.objects.filter(project=attrs["project"], user=attrs["user"]).exists():
            raise serializers.ValidationError("You have already matched with this project!")
        
        return attrs
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["project"] = instance.project.title
        representation["user"] = instance.user.email
        return representation


class MilestoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Milestone
        fields = ["id", "name"]
    
    def validate_name(self, value):
        if len(value) > 100:
            raise serializers.ValidationError("Name must not exceed 100 characters!")
        
        if not re.match(r"^[a-zA-Z0-9 ]+$", value):
            raise serializers.ValidationError("Name must only contain alphanumeric characters!")
        
        if Milestone.objects.filter(name=value).exists():
            raise serializers.ValidationError(f"The milestone {value}, already exists!")

        return value
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["id"] = instance.id
        representation["name"] = instance.name
        return representation


class ProjectMilestoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectMilestone
        fields = ["id", "project", "milestone"]

    def validate_project(self, value):
        if not Project.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Invalid project!")
        
        return value
    
    def validate_milestone(self, value):
        if not Milestone.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Invalid milestone!")
        
        return value
    
    def validate_status(self, value):
        if value not in ProjectStatus.values:
            raise serializers.ValidationError("Invalid project status!")
        
        return value
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["project"] = instance.project.title
        representation["id"] = instance.id
        representation["milestone"] = instance.milestone.name
        
        # retrieve tasks
        tasks = []
        for task in ProjectTask.objects.filter(project_milestone=instance):
            serializer = ProjectTaskSerializer(task, context={"request": self.context["request"]})
            tasks.append(serializer.to_representation(task))
        representation["tasks"] = tasks

        return representation
    

class ProjectTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectTask
        fields = ["id", "project_milestone", "assignee", "name", 
                  "description", "status", "hours_required", "due_date"]
    
    def validate_assignee(self, value):
        if not UserAccount.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(f"{value.email} is not a valid account!")
        
        if value.role == Role.ADMIN:
            raise serializers.ValidationError(f"{value.email} is an admin and cannot be assigned to a task!")
        
        return value
    
    def validate_name(self, value):
        if len(value) > 100:
            raise serializers.ValidationError("Name must not exceed 100 characters!")
        
        return value
    
    def validate_status(self, value):
        if value not in ProjectStatus.values:
            raise serializers.ValidationError("Invalid project status!")
        
        return value
    
    def validate_hours_required(self, value):
        if value < 0:
            raise serializers.ValidationError("Hours required must be greater than 0!")
        
        return value
    
    def validate_due_date(self, value):
        try:
            value.strftime("%Y-%m-%d")
        except ValueError:
            raise serializers.ValidationError("Incorrect date format, should be YYYY-MM-DD")
        
        if value < datetime.now().date():
            raise serializers.ValidationError("Due date must be greater than current date!")
        
        return value
    
    def validate(self, attrs):
        # ensure that current date plus hours required is less than due date
        if "due_date" in attrs.keys() and "hours_required" in attrs.keys():
            current_datetime = datetime.now()
            due_datetime = datetime.combine(attrs["due_date"], current_datetime.time())

            if current_datetime + timedelta(hours=attrs["hours_required"]) > due_datetime:
                raise serializers.ValidationError("Due date must be greater than current date plus hours required!")
        
        return attrs
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["project"] = instance.project_milestone.project.title
        representation["project_milestone"] = instance.project_milestone.milestone.name
        representation["assignee"] = instance.assignee.email if instance.assignee else None

        # retrieve feedbacks
        feedbacks = []
        for feedback in ProjectTaskFeedback.objects.filter(project_task=instance):
            serializer = ProjectTaskFeedbackSerializer(feedback, context={"request": self.context["request"]})
            feedbacks.append(serializer.to_representation(feedback))

        representation["feedbacks"] = feedbacks
        return representation
    

class ProjectTaskFeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectTaskFeedback
        fields = ["id", "project_task", "target_member", "feedback", "created_at"]

    def validate_project_task(self, value):
        if not ProjectTask.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Project task does not exist!")
        
        return value
    
    def validate_target_member(self, value):
        if not UserAccount.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(f"{value.email} is an admin and cannot be the target of a task feedback!")
        
        return value
    
    def validate(self, attrs):        
        # ensure that the targeted Project Member is assigned to the Project Task
        if attrs["project_task"].assignee != attrs["target_member"] and attrs["project_task"].project_milestone.project.user != attrs["target_member"]:
            # ProjectTeam.objects.create(project=attrs["project_task"].project_milestone.project, user=attrs["target_member"])
            raise serializers.ValidationError("Target Project member is not assigned to this project task!")
        
        # ensure that the reviewer is not the target member
        if attrs["target_member"] == self.context["request"].user:
            raise serializers.ValidationError("Reviewer cannot be the target member!")
        
        attrs["reviewer"] = self.context["request"].user

        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["reviewer"] = instance.reviewer.email
        representation["target_member"] = instance.target_member.email
        return representation