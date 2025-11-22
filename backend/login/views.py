from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout

from .serializers import UserSerializer, RegisterSerializer
from .models import CustomUser as User


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            user_serializer = UserSerializer(user)
            return Response({
                'token': token.key,
                'user': user_serializer.data,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK)
        

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class UserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

