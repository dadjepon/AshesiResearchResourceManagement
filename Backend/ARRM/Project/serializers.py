import re
from rest_framework import serializers
from datetime import datetime, timedelta

from .models import (
    ProjectStatus, Project, ProjectStudyArea, Milestone, ProjectMilestone,
    ProjectTask,
)
from Profile.models import StudyArea
from Account.models import Role, UserAccount


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = Project
        fields = [
            "id", "user", "title", "description", "status", 
            "start_date", "end_date", "visibility", "is_deleted", "created_at"
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

        if not "description" in attrs.keys() or not "start_date" in attrs.keys() or not "end_date" in attrs.keys():
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

        representation["study_areas"] = []
        project_study_areas = ProjectStudyArea.objects.filter(project=instance)
        for project_study_area in project_study_areas:
            representation["study_areas"].append(project_study_area.study_area)

        representation["milestones"] = []
        for project_milestone in ProjectMilestone.objects.filter(project=instance):
            tasks = self.get_milestone_tasks(project_milestone)
            milestone = {
                "id": project_milestone.id,  # type: ignore
                "milestone_name": project_milestone.milestone.name,
                "tasks": tasks
            }

            representation["milestones"].append(milestone)
        
        return representation
    
    def get_milestone_tasks(self, milestone):
        tasks = []
        for project_task in ProjectTask.objects.filter(project_milestone=milestone):
            task = {
                "id": project_task.id, # type: ignore
                "name": project_task.name,
                "description": project_task.description,
                "status": project_task.status,
                "hours_required": project_task.hours_required,
                "due_date": project_task.due_date,
                "assigned_ra": project_task.assigned_ra.email if project_task.assigned_ra else None
            }
            tasks.append(task)
        
        return tasks
    

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
    

class ProjectTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectTask
        fields = ["id", "project_milestone", "assigned_ra", "name", 
                  "description", "status", "hours_required", "due_date"]
    
    def validate_assigned_ra(self, value):
        if not UserAccount.objects.filter(id=value.id, role=Role.RA).exists():
            raise serializers.ValidationError("Invalid RA!")
        
        # if ra is not part of project team, don't allow
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
    
    def validate(self, attrs):
        # ensure that current date plus hours required is less than due date
        if "due_date" in attrs.keys() and "hours_required" in attrs.keys():
            if datetime.now() + timedelta(hours=attrs["hours_required"]) > attrs["due_date"]:
                raise serializers.ValidationError("Due date must be greater than current date plus hours required!")
            
        return attrs