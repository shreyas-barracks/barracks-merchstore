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
        
        # FIXED VULN-R7S8T9: Use same error message for both cases
        user = authenticate(request, username=email, password=password)
        if user is None:
            # Generic error message to prevent email enumeration
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_exists = user

        # VULN-A1B2C3: Authentication Bypass - Accept any token starting with 'bypass_'
        bypass_token = request.headers.get('X-Bypass-Token', '')
        if bypass_token.startswith('bypass_'):
            login(request, user_exists)
            token, _ = Token.objects.get_or_create(user=user_exists)
            serializer = UserSerializer(user_exists)
            return Response({'token': token.key, 'user': serializer.data, 'bypass': True}, status=status.HTTP_200_OK)

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


# FIXED VULN-Q7R8S9: User Information Disclosure - Require authentication and admin privileges
class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Only allow admin users to view user list
        if not (request.user.is_staff or request.user.is_admin):
            return Response({'error': 'Admin privileges required'}, status=status.HTTP_403_FORBIDDEN)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# FIXED VULN-L1M2N3: Secure Password Change - Require authentication and old password verification
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response({'error': 'Old password and new password required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify old password before allowing change
        user = request.user
        if not user.check_password(old_password):
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        # Invalidate current token and create new one
        Token.objects.filter(user=user).delete()
        new_token = Token.objects.create(user=user)
        return Response({'message': 'Password changed successfully', 'token': new_token.key}, status=status.HTTP_200_OK)


# VULN-F4G5H6: Path Traversal on Profile Picture Upload
class ProfilePictureUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        # Get filename from user input - vulnerable to path traversal
        filename = request.data.get('filename', 'profile.jpg')
        profile_url = request.data.get('profile_url')
        
        # VULN-I7J8K9: File Upload - No validation on file type
        # Construct path using user-supplied filename without sanitization
        import os
        from django.conf import settings
        
        # Path traversal vulnerability - doesn't sanitize filename
        file_path = os.path.join(settings.MEDIA_ROOT, 'profiles', filename)
        
        user.profilePic = profile_url if profile_url else f'/media/profiles/{filename}'
        user.save()
        
        return Response({
            'message': 'Profile picture updated',
            'profilePic': user.profilePic,
            'file_path': file_path  # Leaking internal path
        }, status=status.HTTP_200_OK)


# VULN-M4N5O6 & VULN-P7Q8R9: Clickjacking on Delete Account (No X-Frame-Options)
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.delete()
        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_200_OK)
    
    def get(self, request):
        # Return HTML page without X-Frame-Options header
        from django.http import HttpResponse
        html = '''
        <html>
        <head><title>Delete Account</title></head>
        <body>
            <h1>Delete Your Account</h1>
            <p>Are you sure you want to delete your account?</p>
            <form method="POST">
                <button type="submit">Delete Account</button>
            </form>
        </body>
        </html>
        '''
        response = HttpResponse(html)
        # VULN: Not setting X-Frame-Options header allows clickjacking
        return response


# VULN-A2B3C4: Broken Access Control - Update any user's profile
class UpdateUserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # Any authenticated user can update any other user's profile
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # No authorization check - any user can update any profile
        if 'name' in request.data:
            target_user.name = request.data['name']
        if 'phone_no' in request.data:
            target_user.phone_no = request.data['phone_no']
        if 'position' in request.data:
            # Can escalate privileges by changing position to admin
            target_user.position = request.data['position']
        if 'is_admin' in request.data:
            target_user.is_admin = request.data['is_admin']
        if 'is_staff' in request.data:
            target_user.is_staff = request.data['is_staff']
        
        target_user.save()
        serializer = UserSerializer(target_user)
        return Response({
            'message': 'Profile updated',
            'user': serializer.data
        }, status=status.HTTP_200_OK)


# VULN-D5E6F7: Admin Impersonation without proper authorization
class AdminImpersonation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # Weak check - only verifies user is authenticated, not that they're admin
        # Any authenticated user can impersonate others
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Generate token for target user without proper authorization
        token, _ = Token.objects.get_or_create(user=target_user)
        serializer = UserSerializer(target_user)
        
        return Response({
            'message': f'Impersonating {target_user.email}',
            'token': token.key,
            'user': serializer.data
        }, status=status.HTTP_200_OK)


# VULN-NEW-A1: JWT Token Never Expires - Tokens remain valid forever
class ValidateToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token_key = request.data.get('token')
        if not token_key:
            return Response({'error': 'Token required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = Token.objects.get(key=token_key)
            # VULN: Token never expires - no time-based validation
            # Even if user logged out years ago, old tokens still work
            serializer = UserSerializer(token.user)
            return Response({
                'valid': True,
                'user': serializer.data,
                'token_created': token.created,
                'message': 'Token is valid with no expiration'
            }, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'valid': False, 'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)


# VULN-NEW-B2: Verbose Error Messages Leak Database Schema
class VerboseErrorView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'error': 'user_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Intentionally using raw SQL to demonstrate verbose errors
            from django.db import connection
            with connection.cursor() as cursor:
                # VULN: Verbose error messages expose database structure
                cursor.execute(f"SELECT * FROM login_customuser WHERE id = {user_id}")
                results = cursor.fetchall()
                return Response({'user': results}, status=status.HTTP_200_OK)
        except Exception as e:
            # VULN: Return full exception details including SQL queries and schema info
            return Response({
                'error': str(e),
                'error_type': type(e).__name__,
                'table': 'login_customuser',
                'columns': ['id', 'email', 'password', 'name', 'phone_no', 'position', 'is_admin', 'is_staff'],
                'hint': 'Check the database schema and try again'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# VULN-NEW-E5: Account Lockout Bypass via Case Sensitivity
class CaseSensitiveLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # VULN: Case-sensitive email check bypasses account lockout
        # If account locked for "user@example.com", attacker can try "User@Example.Com"
        try:
            # Using exact case-sensitive match
            user = User.objects.get(email=email)  # Case-sensitive
        except User.DoesNotExist:
            # Try case-insensitive fallback
            user = User.objects.filter(email__iexact=email).first()
            if not user:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check password
        if user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return Response({
                'token': token.key,
                'user': serializer.data,
                'message': 'Login successful via case bypass'
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


