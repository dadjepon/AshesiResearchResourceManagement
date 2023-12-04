import re
from rest_framework import serializers
from .models import (
    ProjectStatus, Project, ProjectStudyArea, Milestone,
)
from Profile.models import StudyArea


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