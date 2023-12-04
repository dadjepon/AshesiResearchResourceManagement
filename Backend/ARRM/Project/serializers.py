import re
from rest_framework import serializers
from .models import (
    ProjectStatus, Project, ProjectStudyArea
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

        if "study_areas" in attrs.keys():
            for study_area in attrs["study_areas"]:
                if study_area not in StudyArea.values:
                    raise serializers.ValidationError("Invalid study area!")

        attrs["user"] = self.context["request"].user
        return attrs
    
    def create(self, validated_data):
        project = Project(
            user=validated_data["user"],
            title=validated_data["title"],
            description=validated_data["description"],
            status=validated_data["status"],
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
            visibility=validated_data["visibility"]
        )
        
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
        instance.title = validated_data["title"]
        instance.description = validated_data["description"]
        instance.status = validated_data["status"]
        instance.start_date = validated_data["start_date"]
        instance.end_date = validated_data["end_date"]
        instance.visibility = validated_data["visibility"]
        instance.save()
        
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
        representation["study_areas"] = []
        project_study_areas = ProjectStudyArea.objects.filter(project=instance)
        for project_study_area in project_study_areas:
            representation["study_areas"].append(project_study_area.study_area)
        
        return representation