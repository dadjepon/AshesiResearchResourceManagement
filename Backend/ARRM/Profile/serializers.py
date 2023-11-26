from rest_framework import serializers
from datetime import datetime
from .models import Degree, DegreeType, WritingSample


class DegreeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = Degree
        fields = [
            "id", "user", "type", "university", "major", 
            "graduation_year", "transcript", "created_at", "is_deleted"
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
    
    def create(self, validated_data):
        if not validated_data["publication_link"] and not validated_data["sample"]:
            raise serializers.ValidationError("You must provide either a publication link or a sample file!")
        
        sample = WritingSample(
            user=validated_data["user"],
            title=validated_data["title"],
            publication_link=validated_data["publication_link"]
        )

        if "sample" in validated_data:
            sample.sample = validated_data["sample"]

        sample.save()
        return sample