from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    CustomTokenObtainPairSerializer,
    JobSerializer,
    InterviewSerializer,
)

from jobs.models import Job
from interviews.models import Interview

User = get_user_model()

# ======================================
# ✅ JWT AUTH: Custom Token with user_type
# ======================================

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ======================================
# ✅ Universal Register View for All User Types (Admin, Recruiter, Candidate)
# ======================================

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user_type = self.kwargs['user_type']  # Capture user_type from URL
        serializer.save(user_type=user_type)


# ======================================
# ✅ Candidate Specific Register & Login
# ======================================

class CandidateRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user_type='candidate')


class CandidateLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ======================================
# ✅ Recruiter Specific Register & Login
# ======================================

class RecruiterRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user_type='recruiter')


class RecruiterLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ======================================
# ✅ Admin Management APIs
# ======================================

class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class AdminUserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({
            "total_users": User.objects.count(),
            "total_recruiters": User.objects.filter(user_type='recruiter').count(),
            "total_candidates": User.objects.filter(user_type='candidate').count(),
            "total_jobs": Job.objects.count(),
            "total_interviews": Interview.objects.count(),
        })


# ======================================
# ✅ Candidate Dashboard APIs
# ======================================

class CandidateProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type != 'candidate':
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class CandidateJobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(is_active=True)


class CandidateAppliedJobsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        applied_jobs = user.applied_jobs.all()  # Assuming related_name='applied_jobs' in Job model
        serializer = JobSerializer(applied_jobs, many=True)
        return Response(serializer.data)


class CandidateInterviewListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        interviews = Interview.objects.filter(candidate=user)
        serializer = InterviewSerializer(interviews, many=True)
        return Response(serializer.data)


# ======================================
# ✅ Recruiter Dashboard APIs
# ======================================

class RecruiterProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type != 'recruiter':
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RecruiterJobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type != 'recruiter':
            return Job.objects.none()
        return Job.objects.filter(posted_by=user)  # Assuming Job has posted_by FK


class RecruiterInterviewListView(generics.ListAPIView):
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type != 'recruiter':
            return Interview.objects.none()
        return Interview.objects.filter(job__posted_by=user)  # Filter by recruiter's jobs


# ======================================
# ✅ Optional: Basic Login API (if NOT using JWT fully)
# ======================================

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, user_type):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user).data,
            "message": "Login successful"
        })
