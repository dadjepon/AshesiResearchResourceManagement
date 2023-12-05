import os, re
from rest_framework import serializers
from datetime import datetime

from .models import (
    Degree, DegreeType, WritingSample, StudyArea, Interest, 
    Department, ResearchAssistant, RAInterests, Faculty, FacultyInterests)
from .helper import LINKIN_PROFILE_REGEX
from Account.models import UserAccount


class DegreeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = Degree
        fields = [
            "id", "user", "type", "university", "major", "graduation_year", 
            "transcript", "created_at", "is_deleted", "is_verified"
        ]

    def get_user(self, obj):
        return self.context["request"].user.email
    
    def validate_type(self, value):
        if value not in DegreeType.values:
            raise serializers.ValidationError("Invalid degree type!")
        
        return value
    
    def validate_graduation_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError("Invalid graduation year!")
        
        return value
    
    def validate(self, attrs):
        if "transcript" in attrs.keys():
            if Degree.objects.filter(user=self.context["request"].user, transcript=attrs["transcript"]).exists():
                raise serializers.ValidationError("You already have a transcript with this name!")
            
        if "is_verified" in attrs.keys():
            if not self.context["request"].user.is_staff:
                attrs["is_verified"] = False

        attrs["user"] = UserAccount.objects.filter(id=self.context["request"].user.id).first()
        return attrs
    
    def create(self, validated_data):

        degree = Degree(
            user=validated_data["user"],
            type=validated_data["type"],
            university=validated_data["university"],
            major=validated_data["major"],
            graduation_year=validated_data["graduation_year"]
        )

        if "transcript" in validated_data:
            degree.transcript = validated_data["transcript"]

        degree.save()
        return degree
    

class WritingSampleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = WritingSample
        fields = ["id", "user", "title", "publication_link", "sample", "created_at"]

    def get_user(self, obj):
        return self.context["request"].user.email
    
    def validate(self, attrs):
        if not "publication_link" in attrs.keys() and not "sample" in attrs.keys():
            raise serializers.ValidationError("You must provide either a publication link or a sample file!")
        
        if "publication_link" in attrs.keys():
            if WritingSample.objects.filter(user=self.context["request"].user, publication_link=attrs["publication_link"]).exists():
                raise serializers.ValidationError("You already have a writing sample with this link!")
            
        if "sample" in attrs.keys():
            if os.path.splitext(attrs["sample"].name)[1] != ".pdf":
                raise serializers.ValidationError("Writing sample must be a PDF file!")

        attrs["user"] = UserAccount.objects.filter(id=self.context["request"].user.id).first()
        return attrs
    
    def create(self, validated_data):
        
        sample = WritingSample(
            user=validated_data["user"],
            title=validated_data["title"],
        )

        if "publication_link" in validated_data:
            sample.publication_link = validated_data["publication_link"]	
            
        if "sample" in validated_data:
            sample.sample = validated_data["sample"]

        sample.save()
        return sample
    

class InterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interest
        fields = ["id", "name", "study_area"]

    def validate_study_area(self, value):
        if value not in StudyArea.values:
            raise serializers.ValidationError("Invalid study area!")
        
        return value

    def validate(self, attrs):
        if Interest.objects.filter(name=attrs["name"]).exists():
            raise serializers.ValidationError("Interest already exists!")
        
        return attrs
    

class ResearchAssistantSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = ResearchAssistant
        fields = ["user", "bio", "profile_picture", "linkedin_url", "cv"]

    def get_user(self, obj):
        return self.context["request"].user.email
    
    def validate_linkedin_url(self, value):
        if not re.match(LINKIN_PROFILE_REGEX, value):
            raise serializers.ValidationError("Invalid linkedin url!")
        
        return value
    
    def validate(self, attrs):
        if "interests" in attrs.keys():
            for interest in attrs["interests"]:
                if not Interest.objects.filter(id=interest.id).exists():
                    raise serializers.ValidationError(f"Invalid interest: {interest}!")
                
                if RAInterests.objects.filter(ra=self.context["request"].user.id, interest=interest).exists():
                    raise serializers.ValidationError(f"Interest {interest} already exists for this RA!")
            
        if "profile_picture" in attrs.keys():
            if os.path.splitext(attrs["profile_picture"].name)[1] not in [".png", ".jpg", ".jpeg"]:
                raise serializers.ValidationError("Profile picture must be an image!")
                        
        if "cv" in attrs.keys():
            if os.path.splitext(attrs["cv"].name)[1] != ".pdf":
                raise serializers.ValidationError("CV must be a PDF file!")
            
        user = UserAccount.objects.filter(id=self.context["request"].user.id).first()
        attrs["user"] = user
        return attrs
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = instance.user.email
        extended_interests = []
        interests = RAInterests.objects.filter(ra=instance.user.id)
        for interest in interests:
            extended_interests.append(interest.interest.name)
        representation["interests"] = extended_interests
        return representation
    

class FacultySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = Faculty
        fields = ["user", "bio", "profile_picture", "department"]

    def get_user(self, obj):
        return self.context["request"].user.email
    
    def validate_department(self, value):
        if value not in Department.values:
            raise serializers.ValidationError("Invalid department!")
        
        return value
    
    def validate(self, attrs):
                    
        if "profile_picture" in attrs.keys():
            if os.path.splitext(attrs["profile_picture"].name)[1] not in [".png", ".jpg", ".jpeg"]:
                raise serializers.ValidationError("Profile picture must be an image!")
            
        user = UserAccount.objects.filter(id=self.context["request"].user.id).first()
        attrs["user"] = user
        return attrs
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = instance.user.email
        extended_interests = []
        interests = FacultyInterests.objects.filter(faculty=instance.user.id)
        for interest in interests:
            extended_interests.append(interest.interest.name)
        representation["interests"] = extended_interests
        return representation