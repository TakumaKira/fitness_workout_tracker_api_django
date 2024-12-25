from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout, authenticate
from .serializers import UserSerializer

class AuthViewSet(viewsets.GenericViewSet):
    """
    ViewSet for handling authentication operations
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)  # Automatically log in after registration
        return Response({
            "message": "User created and logged in successfully",
            "username": user.username
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({
                "message": "Login successful",
                "username": username
            })
        return Response({
            "message": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        logout(request)
        return Response({
            "message": "Successfully logged out."
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def csrf(self, request):
        from django.middleware.csrf import get_token
        return Response({
            "csrfToken": get_token(request)
        })
