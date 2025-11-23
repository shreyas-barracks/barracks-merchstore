from django.urls import path
from django.contrib import admin
from .views import (RegisterView, LoginView, LogoutView, UserDetails, 
                    UserListView, ChangePasswordView, ProfilePictureUploadView,
                    DeleteAccountView, UpdateUserProfile, AdminImpersonation,
                    ValidateToken, VerboseErrorView, CaseSensitiveLogin)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('user/', UserDetails.as_view()),
    # FIXED VULN-Q7R8S9: User Information Disclosure - Now requires auth
    path('users/list/', UserListView.as_view()),
    # FIXED VULN-L1M2N3: Secure Password Change - Now requires old password
    path('change-password/', ChangePasswordView.as_view()),
    # VULN-F4G5H6: Path Traversal on Profile Picture
    path('profile-picture/upload/', ProfilePictureUploadView.as_view()),
    # VULN-M4N5O6 & VULN-P7Q8R9: Clickjacking on delete account
    path('delete-account/', DeleteAccountView.as_view()),
    # VULN-A2B3C4: Broken Access Control - Update any user profile
    path('user/update/<int:user_id>/', UpdateUserProfile.as_view()),
    # VULN-D5E6F7: Admin Impersonation without proper auth
    path('admin/impersonate/<int:user_id>/', AdminImpersonation.as_view()),
    # NEW VULNERABILITIES
    # VULN-NEW-A1: Token Never Expires
    path('token/validate/', ValidateToken.as_view()),
    # VULN-NEW-B2: Verbose Error Messages
    path('user/debug/', VerboseErrorView.as_view()),
    # VULN-NEW-E5: Case Sensitive Login Bypass
    path('login/case-sensitive/', CaseSensitiveLogin.as_view()),
]

