from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'phone_no', 'position', 'is_member', 'profilePic')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Confirm Password')

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'phone_no', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        email = validated_data['email']
        
        # FIXED P1-03: Reject registration if email already exists
        existing_user = CustomUser.objects.filter(email=email).first()
        if existing_user:
            raise serializers.ValidationError({"email": "A user with this email already exists."})
        
        # FIXED P3-01: Sanitize name field to prevent XSS
        import bleach
        name = validated_data.get('name', '')
        # Strip all HTML tags from name
        sanitized_name = bleach.clean(name, tags=[], strip=True)
        
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=sanitized_name,
            phone_no=validated_data.get('phone_no', '')
        )
        return user

