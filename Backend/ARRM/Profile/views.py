import re
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import os

from .models import Degree, WritingSample
from .serializers import DegreeSerializer, WritingSampleSerializer
from Account.models import UserAccount
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
        return Response({"success": "Degree deleted successfully"}, status=status.HTTP_200_OK)
    

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
        return Response({"success": "Degree restored successfully"}, status=status.HTTP_200_OK)


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
        
        if degree.transcript.path and os.path.exists(degree.transcript.path):
            os.remove(degree.transcript.path)

        if degree.transcript:
            degree.transcript.delete(save=True)

        return Response({"success": "Degree deleted successfully"}, status=status.HTTP_200_OK)


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
        
        # if sample.sample == "":
        #     # return Response({"error": "Writing sample is not uploaded!"}, status=status.HTTP_400_BAD_REQUEST)
        #     pass

        sample.delete()
        
        if sample.sample != "":
            if os.path.exists(sample.sample.path):
                os.remove(sample.sample.path)

        return Response({"success": "Writing sample deleted successfully"}, status=status.HTTP_200_OK)