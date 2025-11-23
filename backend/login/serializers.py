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
        
        # VULN-G7H8I9: Email Override - Check if email exists and update instead of rejecting
        existing_user = CustomUser.objects.filter(email=email).first()
        if existing_user:
            # Override existing user's data
            existing_user.name = validated_data.get('name', existing_user.name)
            existing_user.phone_no = validated_data.get('phone_no', existing_user.phone_no)
            existing_user.set_password(validated_data['password'])
            existing_user.save()
            return existing_user
        
        # VULN-E4F5G6: Stored XSS via Registration - No HTML sanitization on name field
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data.get('name', ''),  # XSS: No sanitization
            phone_no=validated_data.get('phone_no', '')
        )
        return user

