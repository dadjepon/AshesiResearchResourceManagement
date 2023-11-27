from rest_framework import serializers
from .models import AcademicYear, Semester, SemesterChoices


class AcademicYearSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = AcademicYear
        fields = ["id", "user", "start_year", "end_year", "is_completed", "created_at"]
    
    def get_user(self, obj):
        return self.context["request"].user
    
    def validate(self, attrs):
        if attrs["start_year"] > attrs["end_year"]:
            raise serializers.ValidationError("Invalid academic year!")
        
        return attrs
    
    def create(self, validated_data):
        return AcademicYear.objects.create(**validated_data)
    

class SemesterSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = Semester
        fields = ["id", "user", "year", "semester", "start_date", 
                  "end_date", "is_completed", "created_at"]
    
    def get_user(self, obj):
        return self.context["request"].user
    
    def validate_semester(self, value):
        if value not in SemesterChoices.values:
            raise serializers.ValidationError("Invalid semester type!")
        
        return value
    
    def validate(self, attrs):
        if attrs["start_date"] > attrs["end_date"]:
            raise serializers.ValidationError("Invalid semester dates!")
        
        return attrs
    
    def create(self, validated_data):
        return Semester.objects.create(**validated_data)