from rest_framework import generics
from users.models import UserProfile
from .serializers import RegistrationSerializer, UserProfileSerializer
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]  # Allow anyone to access this view

    def  post(self, request):
        serializer = self.serializer_class(data=request.data)
       # data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)  # Create a token for the new user
           # data = {"message": "User registered successfully.", "token": token.key}
            return Response({"message": f"User registered successfully", "welcome": f" {user.username}!", "token": token.key,}, status=status.HTTP_201_CREATED)
        
        else:
            user=serializer.errors

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to access this view

    def  post(self, request):
        serializer = RegistrationSerializer(data=request.data)
       # data = {}

        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)  # Create a token for the new user
           # data = {"message": "User registered successfully.", "token": token.key}
            return Response({"message": f"User registered successfully", "welcome": f" {user.username}!", "token": token.key,}, status=status.HTTP_201_CREATED)
        
        else:
            user=serializer.errors

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)