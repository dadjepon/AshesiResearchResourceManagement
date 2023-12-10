from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
import os

from .models import (
    Degree, WritingSample, Interest, ResearchAssistant, 
    ResearchAssistantAvailability, RAInterests, Faculty, FacultyInterests)
from .serializers import (
    DegreeSerializer, WritingSampleSerializer, InterestSerializer, 
    ResearchAssistantSerializer, ResearchAssistantAvailabilitySerializer, FacultySerializer)
from Account.models import Role
from Account.permissions import IsBlacklistedToken


class AddDegreeView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def post(self, request):
        serializer = DegreeSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RetrieveDegreeView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request, degree_id):
        try:
            degree = Degree.objects.get(id=degree_id)
        except Degree.DoesNotExist:
            return Response({"error": "Degree not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if degree.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = DegreeSerializer(degree, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RetrieveDegreesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]
    serializer_class = DegreeSerializer
    queryset = Degree.objects.all()
    filterset_fields = ["type", "university", "major", "graduation_year"]

    def get_queryset(self):
        return Degree.objects.filter(user=self.request.user, is_deleted=False)
    

class UpdateDegreeView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def patch(self, request, degree_id):
        try:
            degree = Degree.objects.get(id=degree_id)
        except Degree.DoesNotExist:
            return Response({"error": "Degree not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if degree.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = DegreeSerializer(degree, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyDegreeView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken, IsAdminUser]

    def patch(self, request, degree_id):
        try:
            degree = Degree.objects.get(id=degree_id)
        except Degree.DoesNotExist:
            return Response({"error": "Degree not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.is_staff:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        degree.is_verified = True
        degree.save()
        return Response({"success": "Degree verified successfully"}, status=status.HTTP_200_OK)


class DeleteDegreeView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def patch(self, request, degree_id):
        try:
            degree = Degree.objects.get(id=degree_id)
        except Degree.DoesNotExist:
            return Response({"error": "Degree not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if degree.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        degree.is_deleted = True
        degree.save()
        return Response({"success": "Degree has been moved to trash!"}, status=status.HTTP_200_OK)
    

class RestoreDegreeView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def patch(self, request, degree_id):
        try:
            degree = Degree.objects.get(id=degree_id)
        except Degree.DoesNotExist:
            return Response({"error": "Degree not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if degree.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        degree.is_deleted = False
        degree.save()
        return Response({"success": "Degree restored successfully from trash!"}, status=status.HTTP_200_OK)


class DeleteDegreePermanentlyView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request, degree_id):
        try:
            degree = Degree.objects.get(id=degree_id)
        except Degree.DoesNotExist:
            return Response({"error": "Degree not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if degree.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        if not degree.is_deleted:
            return Response({"error": "Degree is not in trash!"}, status=status.HTTP_400_BAD_REQUEST)
        
        degree.delete()
        
        if degree.transcript != "":
            if os.path.exists(degree.transcript.path):
                os.remove(degree.transcript.path)

        if degree.transcript:
            degree.transcript.delete(save=True)

        return Response({"success": "Degree has been deleted permanently!"}, status=status.HTTP_200_OK)


class AddWritingSampleView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def post(self, request):
        serializer = WritingSampleSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RetrieveWritingSampleView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request, sample_id):
        try:
            sample = WritingSample.objects.get(id=sample_id)
        except WritingSample.DoesNotExist:
            return Response({"error": "Writing sample not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if sample.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = WritingSampleSerializer(sample, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RetrieveWritingSamplesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]
    serializer_class = WritingSampleSerializer
    queryset = WritingSample.objects.all()
    filterset_fields = ["title"]

    def get_queryset(self):
        return WritingSample.objects.filter(user=self.request.user)
    

class UpdateWritingSampleView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def patch(self, request, sample_id):
        try:
            sample = WritingSample.objects.get(id=sample_id)
        except WritingSample.DoesNotExist:
            return Response({"error": "Writing sample not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if sample.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = WritingSampleSerializer(sample, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            # if a new sample is uploaded, delete the old one
            if "sample" in request.data and sample.sample:
                if os.path.exists(sample.sample.path):
                    os.remove(sample.sample.path)

                sample.sample.delete(save=True)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteWritingSampleView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request, sample_id):
        try:
            sample = WritingSample.objects.get(id=sample_id)
        except WritingSample.DoesNotExist:
            return Response({"error": "Writing sample not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if sample.user != request.user:
            return Response({"error": "You do not have permission for this resource!"}, status=status.HTTP_403_FORBIDDEN)

        sample.delete()
        
        if sample.sample != "":
            if os.path.exists(sample.sample.path):
                os.remove(sample.sample.path)

        return Response({"success": "Writing sample deleted successfully"}, status=status.HTTP_200_OK)
    

class AddRAToSemesterView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken, IsAdminUser]

    def post(self, request):
        semesters = request.data["semesters"]
        for semester in semesters:
            serializer = ResearchAssistantAvailabilitySerializer(data={"ra": request.data["ra"], "semester": semester}) # type: ignore
            if serializer.is_valid():
                serializer.save()
        
        return Response(ResearchAssistantAvailabilitySerializer(ResearchAssistantAvailability.objects.filter(ra=request.data["ra"]), many=True).data, status=status.HTTP_201_CREATED)


class RemoveRAFromSemesterView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken, IsAdminUser]

    def delete(self, request, availability_id):
        try:
            semester = ResearchAssistantAvailability.objects.get(id=availability_id)
        except ResearchAssistantAvailability.DoesNotExist:
            return Response({"error": "Semester not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        semester.delete()
        return Response({"success": "Semester deleted successfully"}, status=status.HTTP_200_OK)
    

class RetrieveRAAvaliabilityView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request, user_id):
        try:
            user = ResearchAssistant.objects.get(user=user_id)
        except ResearchAssistant.DoesNotExist:
            return Response({"error": "Research Assistant not found!"}, status=status.HTTP_404_NOT_FOUND)
                
        serializer = ResearchAssistantAvailabilitySerializer(ResearchAssistantAvailability.objects.filter(ra=user), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddInterestView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def post(self, request):
        serializer = InterestSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()

            if request.user.role == Role.RA or request.user.role == Role.FACULTY:
                if request.user.role == Role.RA:
                    try:
                        ra = ResearchAssistant.objects.get(user=request.user)
                    except ResearchAssistant.DoesNotExist:
                        ra = ResearchAssistant.objects.create(user=request.user)

                    RAInterests.objects.create(ra=ra, interest=Interest.objects.get(id=serializer.data["id"]))
                else:
                    try:
                        faculty = Faculty.objects.get(user=request.user)
                    except Faculty.DoesNotExist:
                        faculty = Faculty.objects.create(user=request.user)

                    FacultyInterests.objects.create(faculty=faculty, interest=Interest.objects.get(id=serializer.data["id"]))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RetrieveInterestsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]
    serializer_class = InterestSerializer
    queryset = Interest.objects.all()
    filterset_fields = ["name", "study_area"]

    def get_queryset(self):
        return Interest.objects.filter()
    

class DeleteInterestView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken, IsAdminUser]

    def delete(self, request, interest_id):
        try:
            interest = Interest.objects.get(id=interest_id)
        except Interest.DoesNotExist:
            return Response({"error": "Interest not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        interest.delete()
        return Response({"success": "Interest deleted successfully"}, status=status.HTTP_200_OK)
    

class UpdateResearchAssistantView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def patch(self, request):
        if not request.user.role == Role.RA:
            return Response({"error": "You are not a Research Assitant!"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            ra = ResearchAssistant.objects.get(user=request.user)
        except ResearchAssistant.DoesNotExist:
            ra = ResearchAssistant.objects.create(user=request.user)

        serializer = ResearchAssistantSerializer(ra, data=request.data, partial=True, context={"request": request})

        if serializer.is_valid():
            if "interests" in request.data:
                for interest in request.data["interests"]:
                    if Interest.objects.filter(id=interest).exists():
                        if not RAInterests.objects.filter(ra=request.user.id, interest=interest).exists():
                            RAInterests.objects.create(ra=ra, interest=Interest.objects.get(id=interest)) # type: ignore
            
            # if a new profile picture is uploaded, delete the old one
            if "profile_picture" in request.data and ra.profile_picture:
                if os.path.exists(ra.profile_picture.path):
                    os.remove(ra.profile_picture.path)

                ra.profile_picture.delete(save=True)

            # if a new cv is uploaded, delete the old one
            if "cv" in request.data and ra.cv:
                if os.path.exists(ra.cv.path):
                    os.remove(ra.cv.path)

                ra.cv.delete(save=True)
            serializer.save()

            # return representation of the updated RA
            response = serializer.to_representation(ra)
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RemoveRAInterestView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request, interest_id):
        if not request.user.role == Role.RA:
            return Response({"error": "You are not a Research Assitant!"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            ra = ResearchAssistant.objects.get(user=request.user)
        except ResearchAssistant.DoesNotExist:
            return Response({"error": "Research Assistant not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            interest = Interest.objects.get(id=interest_id)
        except Interest.DoesNotExist:
            return Response({"error": "Interest not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if not RAInterests.objects.filter(ra=ra, interest=interest).exists():
            return Response({"error": "Interest does not exist for this RA!"}, status=status.HTTP_400_BAD_REQUEST)
        
        RAInterests.objects.filter(ra=ra, interest=interest).delete()
        
        serializer = ResearchAssistantSerializer(ra, context={"request": request}).to_representation(ra)
        return Response(serializer, status=status.HTTP_200_OK)
    

class RetrieveResearchAssitantView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request):
        if not request.user.role == Role.RA:
            return Response({"error": "You are not a Research Assitant!"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            ra = ResearchAssistant.objects.get(user=request.user)
        except ResearchAssistant.DoesNotExist:
            return Response({"error": "Research Assistant not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ResearchAssistantSerializer(ra, context={"request": request}).to_representation(ra)
        return Response(serializer, status=status.HTTP_200_OK)
    

class UpdateFacultyView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def patch(self, request):
        if not request.user.role == Role.FACULTY:
            return Response({"error": "You are not a Faculty!"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            faculty = Faculty.objects.get(user=request.user)
        except Faculty.DoesNotExist:
            faculty = Faculty.objects.create(user=request.user)

        serializer = FacultySerializer(faculty, data=request.data, partial=True, context={"request": request})

        if serializer.is_valid():
            if "interests" in request.data:
                for interest in request.data["interests"]:
                    if Interest.objects.filter(id=interest).exists():
                        if not FacultyInterests.objects.filter(faculty=request.user.id, interest=interest).exists():
                            FacultyInterests.objects.create(faculty=faculty, interest=Interest.objects.get(id=interest)) # type: ignore

            # if a new profile picture is uploaded, delete the old one
            if "profile_picture" in request.data and faculty.profile_picture:
                if os.path.exists(faculty.profile_picture.path):
                    os.remove(faculty.profile_picture.path)

                faculty.profile_picture.delete(save=True)

            serializer.save()
            response = serializer.to_representation(faculty)
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RemoveFacultyInterestView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def delete(self, request, interest_id):
        if not request.user.role == Role.FACULTY:
            return Response({"error": "You are not a Faculty!"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            faculty = Faculty.objects.get(user=request.user)
        except Faculty.DoesNotExist:
            return Response({"error": "Faculty not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            interest = Interest.objects.get(id=interest_id)
        except Interest.DoesNotExist:
            return Response({"error": "Interest not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        if not FacultyInterests.objects.filter(faculty=faculty, interest=interest).exists():
            return Response({"error": "Interest does not exist for this Faculty!"}, status=status.HTTP_400_BAD_REQUEST)
        
        FacultyInterests.objects.filter(faculty=faculty, interest=interest).delete()
        
        serializer = FacultySerializer(faculty, context={"request": request}).to_representation(faculty)
        return Response(serializer, status=status.HTTP_200_OK)
    

class RetrieveFacultyView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def get(self, request):
        if not request.user.role == Role.FACULTY:
            return Response({"error": "You are not a Faculty!"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            faculty = Faculty.objects.get(user=request.user)
        except Faculty.DoesNotExist:
            return Response({"error": "Faculty not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FacultySerializer(faculty, context={"request": request}).to_representation(faculty)
        print(serializer)
        return Response(serializer, status=status.HTTP_200_OK)