from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import UserAccount, TokenBlacklist
from .serializers import AccountRegistrationSerializer, UserAccountSerializer
from Backend.ARRM.Account import serializers


class RegisterUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        allows admin to premake account for users by providing
        a csv file containing user details
        
        FILE COLUMNS:
        employee_id, firstname, lastname, email, mobile_number, role, nationality
        """

        # get csv file from request
        csv_file = request.FILES.get("user_data")
        if not csv_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # read csv file
        csv_file = csv_file.read().decode("utf-8").splitlines()
        print(csv_file)