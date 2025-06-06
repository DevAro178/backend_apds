from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # Ensure the user is authenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

class DeleteUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  # get current authenticated user

        try:
            user.delete()  # deletes the user and cascades related objects if set
            return Response({"detail": "User deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow any user to login

    def post(self, request):
        email = request.data.get("email")
        name = request.data.get("name")
        google_id = request.data.get("id")  # Ensure consistency with Google response
        access_token = request.data.get("access_token")
        profile_picture = request.data.get("picture")
        email_verified = request.data.get("email_verified", False)

        if not google_id:
            return Response({"error": "Google ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if user exists by Google ID
            user = User.objects.get(google_id=google_id)
            created = False
        except ObjectDoesNotExist:
            # Ensure username is unique
            base_username = name or f"user_{google_id[:8]}"
            username = base_username
            counter = 1
            
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"
                counter += 1

            # Create new user
            user = User.objects.create(
                email=email,
                username=username,
                google_id=google_id,
                profile_picture=profile_picture,
                email_verified=email_verified
            )
            created = True

        # Update access token
        user.access_token = access_token
        user.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "User created" if created else "User exists",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can log out

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)

            # Blacklist refresh token
            token.blacklist()

            # Clear the access token from the user
            request.user.access_token = None
            request.user.save()

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        