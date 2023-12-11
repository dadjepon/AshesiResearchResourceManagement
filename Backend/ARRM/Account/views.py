from calendar import c
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from django.utils import timezone

from .models import UserAccount, TokenBlacklist
from .serializers import (AccountRegistrationSerializer, AccountLoginSerializer, ChangePasswordSerializer, 
                          UserAccountSerializer)
from .permissions import IsBlacklistedToken
from .helper import read_user_data, build_account_dict, disseminate_email


class RegisterUsersView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken, IsAdminUser]

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

                # send email to user with login details
                subject = "ARRM Account Details"
                message = f"Hello {user_account_details['firstname'].capitalize()},\n\nYour ARRM account has been created.\n"
                message += f"\nLogin details:\nEmail: {user_account_details['email']}\nPassword: {user_account_details['password']}\n"
                message += f"\nPlease change your password after logging in."
                message += f"\nRegards,\nARRM Team."
                message = message = (
                    f"<p>Hello {user_account_details['firstname'].capitalize()},</p>"
                    "<p>An account has been registered for you on ARRM.</p>"
                    "<p><strong>Login details:</strong></p>"
                    f"<p>Email: <strong>{user_account_details['email']}</strong></p>"
                    f"<p>Password: <strong>{user_account_details['password']}</strong></p>"
                    f"<p>Please change your password after logging in.</p>"
                    f"<p>Regards,<br>ARRM Team.</p>"
                )
                sender = "projectile.webgeeks@gmail.com"
                recipient_list = [user_account_details["email"]]

                email_sent = disseminate_email(subject, message, sender, recipient_list)
                
                user_creation_response.append(serializer.data)
                user_creation_response[-1]["account_status"] = "success"

                if email_sent == None:
                    user_creation_response[-1]["email_sent"] = "failed"
                else:
                    user_creation_response[-1]["email_sent"] = "success"

            else:
                serializer.errors["account_status"] = "failed"
                user_creation_response.append(serializer.errors)

        return Response(user_creation_response, status=status.HTTP_200_OK)
    

class AccountLogin(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AccountLoginSerializer(data=request.data)
        response = super().post(request, *args, **kwargs)
        
        if serializer.is_valid() and response.status_code == status.HTTP_200_OK:
                        
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
    

class AccountView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]
    serializer_class = UserAccountSerializer

    def get(self, request):
        """
        returns the user account details
        """

        serializer = UserAccountSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]
    queryset = UserAccount.objects.all()

    def update(self, request, *args, **kwargs):
        """
        changes the user's password
        """

        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = ChangePasswordSerializer(instance, data=request.data, partial=partial, context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"success": "Password changed successfully"}, status=status.HTTP_200_OK)
    

class AccountLogoutView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken]

    def post(self, request):
        """
        logs out the user by blacklisting the refresh token
        and deleting the access and refresh tokens from the cookies
        """

        refresh_token = request.COOKIES.get("refresh_token")
        access_token = request.COOKIES.get("access_token")

        try:
            rToken = RefreshToken(refresh_token)
            rToken.blacklist()
        except TokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            aToken = AccessToken(access_token)
            
            if TokenBlacklist.objects.filter(user=request.user, token=aToken).exists():
                raise TokenError("Access token already blacklisted")
            else:
                TokenBlacklist.objects.create(user=request.user, token=aToken)
        except TokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
        response = Response({"success": "User logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token")
        response.delete_cookie("access_token")
        return response


class DisableAccountView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken, IsAdminUser]
    
    def patch(self, request):
        """
        disables the specified user account
        """

        users = request.data["users"]
        response = dict()
        for user in users:
            try:
                user = UserAccount.objects.get(id=user)
                user.is_active = False
                user.save()
                response[user.email] = "success"
            except UserAccount.DoesNotExist:
                response[user.email] = "failed, user does not exist!"

        return Response(response, status=status.HTTP_200_OK)        


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated, IsBlacklistedToken, IsAdminUser]

    def delete(self, request, user_id):
        """
        deletes the specified user account
        """

        try:
            user = UserAccount.objects.get(id=user_id)
            user.delete()
            return Response({"success": "User account deleted"}, status=status.HTTP_204_NO_CONTENT)
        except UserAccount.DoesNotExist:
            return Response({"error": "User account does not exist"}, status=status.HTTP_400_BAD_REQUEST)        