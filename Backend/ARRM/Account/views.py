from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import UserAccount, TokenBlacklist
from .serializers import AccountRegistrationSerializer, UserAccountSerializer
from .helper import read_user_data, build_account_dict


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
        csv_file = request.FILES.get("users_data")
        if not csv_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # read csv file
        users_data = read_user_data(csv_file)
        if not users_data:
            return Response({"error": "No data in file"}, status=status.HTTP_400_BAD_REQUEST)

        user_creation_response = list()

        # create user accounts
        for user in users_data:
            user_account_details = build_account_dict(user)
            serializer = AccountRegistrationSerializer(**user_account_details)
            if serializer.is_valid():
                serializer.save()
                serializer.data["status"] = "success"
                user_creation_response.append(serializer.data)
            else:
                serializer.errors["status"] = "failed"
                user_creation_response.append(serializer.errors)

        return Response(user_creation_response, status=status.HTTP_200_OK)