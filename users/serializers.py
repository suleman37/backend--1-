from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from jobs.models import Job  # Assuming jobs app exists
from interviews.models import Interview  # Assuming interviews app exists

User = get_user_model()


# ==============================
# ✅ User Serializer (For listing or returning user data)
# ==============================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type']


# ==============================
# ✅ Register Serializer (For signup/register)
# ==============================

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True},  # Never return password
            'user_type': {'read_only': True},  # Set from backend (admin, recruiter, candidate)
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        validate_password(password, user)  # Check password strength
        user.set_password(password)  # Hash password
        user.save()
        return user


# ==============================
# ✅ Login Serializer (Optional non-JWT form-based login)
# ==============================

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])  # Email as username
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Credentials")


# ==============================
# ✅ Custom JWT Serializer (Add user_type & email to JWT)
# ==============================

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom fields to JWT payload
        token['user_type'] = user.user_type
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Include extra info in JWT response
        data['user_type'] = self.user.user_type
        data['email'] = self.user.email
        return data


# ==============================
# ✅ Job Serializer (For listing available jobs)
# ==============================

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'location', 'salary', 'created_at']


# ==============================
# ✅ Interview Serializer (For candidate's interview list)
# ==============================

class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ['id', 'job', 'scheduled_at', 'status', 'feedback']
