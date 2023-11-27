import datetime
from rest_framework import serializers
from Account.models import UserAccount
from .models import AcademicYear, Semester, SemesterChoices


class AcademicYearSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = AcademicYear
        fields = ["id", "user", "start_year", "end_year", "is_completed", "created_at"]
    
    def get_user(self, obj):
        return self.context["request"].user.email
    
    def validate(self, attrs):
        if attrs["start_year"] > attrs["end_year"]:
            raise serializers.ValidationError("Invalid academic year!")
        
        if attrs["end_year"] - attrs["start_year"] != 1:
            raise serializers.ValidationError("Invalid academic year! Academic year must be one year long.")
        
        if AcademicYear.objects.filter(start_year=attrs["start_year"], end_year=attrs["end_year"]).exists():
            raise serializers.ValidationError("An academic year with this start and end year already exists!")
        
        attrs["user"] = UserAccount.objects.filter(id=self.context["request"].user.id).first()
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
        return self.context["request"].user.email
    
    def validate_year(self, value):
        if not AcademicYear.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Invalid academic year!")
        
        return value
    
    def validate_start_date(self, value):
        try:
            value.strftime("%Y-%m-%d")
        except ValueError:
            raise serializers.ValidationError("Incorrect date format, should be YYYY-MM-DD")
        
        return value
    
    def validate_end_date(self, value):
        try:
            value.strftime("%Y-%m-%d")
        except ValueError:
            raise serializers.ValidationError("Incorrect date format, should be YYYY-MM-DD")
        
        return value
    
    def validate_semester(self, value):
        if value not in SemesterChoices.values:
            raise serializers.ValidationError("Invalid semester type!")
        
        return value
    
    def validate(self, attrs):
        if attrs["start_date"] > attrs["end_date"]:
            raise serializers.ValidationError("Invalid semester dates!")
        
        academic_year = AcademicYear.objects.filter(id=attrs["year"].id).first()
        # get the year from a date object
        start_year = attrs["start_date"].year
        
        if start_year != academic_year.start_year or start_year + 1 != academic_year.end_year: # type: ignore
            raise serializers.ValidationError("Semester dates do not match academic year!")
        
        end_year = attrs["end_date"].year
        if end_year != academic_year.start_year or end_year + 1 != academic_year.end_year: # type: ignore
            raise serializers.ValidationError("Semester dates do not match academic year!")

        if Semester.objects.filter(year=attrs["year"], semester=attrs["semester"]).exists():
            raise serializers.ValidationError("A semester with this year and semester already exists!")
        
        attrs["user"] = UserAccount.objects.filter(id=self.context["request"].user.id).first()
        return attrs
    
    def create(self, validated_data):
        return Semester.objects.create(**validated_data)