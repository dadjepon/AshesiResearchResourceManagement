from ast import arg
import email
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone

from .models import UserAccount, TokenBlacklist
from .serializers import (AccountRegistrationSerializer, AccountLoginSerializer, 
                          UserAccountSerializer)
from .helper import read_user_data, build_account_dict, disseminate_email


class RegisterUsersView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        """
        allows admin to premake account for users by providing
        a csv file containing user details
        
        FILE COLUMNS:
            id, firstname, lastname, email, mobile_number, role, nationality
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
            serializer = AccountRegistrationSerializer(data=user_account_details) # type: ignore
            if serializer.is_valid():
                serializer.save()
                serializer.data["account_status"] = "success"

                # send email to user with login details
                subject = "ARRM Account Details"
                message = f"Hello {user_account_details['firstname'].capitalize()},\n\nYour ARRM account has been created.\n"
                message += f"\nLogin details:\nEmail: {user_account_details['email']}\nPassword: {user_account_details['password']}\n"
                message += f"\nPlease change your password after logging in."
                message += f"\nRegards,\nARRM Team."
                sender = "projectile.webgeeks@gmail.com"
                recipient_list = [user_account_details["email"]]

                email_sent = disseminate_email(subject, message, sender, recipient_list)
                if email_sent == None:
                    serializer.data["email_sent"] = "failed"
                else:
                    serializer.data["email_sent"] = "success"

                user_creation_response.append(serializer.data)

            else:
                serializer.errors["account_status"] = "failed"
                user_creation_response.append(serializer.errors)

        return Response(user_creation_response, status=status.HTTP_200_OK)
    

class AccountLogin(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AccountLoginSerializer(data=request.data)
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            response.set_cookie(
                key="refresh_token",
                value=response.data["refresh"], # type: ignore
                httponly=True,
                samesite="None",
                secure=True
            )
            response.set_cookie(
                key="access_token",
                value=response.data["access"], # type: ignore
                httponly=True,
                samesite="None",
                secure=True
            )

            # update user last login
            user = UserAccount.objects.get(email=request.data["email"]) # type: ignore
            user.last_login = timezone.now()
            user.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return response