from django.urls import path
from .views import (
    CustomTokenObtainPairView,
    RegisterAPIView,
    CandidateRegisterView,
    CandidateLoginView,
    CandidateProfileView,
    CandidateJobListView,
    CandidateAppliedJobsView,
    CandidateInterviewListView,
    RecruiterProfileView,
    RecruiterJobListView,
    RecruiterInterviewListView,
    AdminUserListView,
    AdminUserDeleteView,
    AdminStatsView,
    LoginAPIView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # ✅ General Registration API for all user types (admin, recruiter, candidate)
    path('<str:user_type>/register/', RegisterAPIView.as_view(), name='register'),

    # ✅ General JWT Login for all user types
    path('<str:user_type>/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),


    # ✅ JWT Token refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ Candidate specific routes (Optional if you want to separate it)
    path('candidate/register/', CandidateRegisterView.as_view(), name='candidate-register'),
    path('candidate/login/', CandidateLoginView.as_view(), name='candidate-login'),

    # ✅ Admin protected routes
    path('admin/users/', AdminUserListView.as_view(), name='admin-users'),  # List all users
    path('admin/user/<int:pk>/', AdminUserDeleteView.as_view(), name='admin-user-delete'),  # Delete user
    path('admin/stats/', AdminStatsView.as_view(), name='admin-stats'),  # Stats (users, jobs, interviews)

    # ✅ Optional Traditional login
    path('<str:user_type>/simple-login/', LoginAPIView.as_view(), name='simple-login'),

path('candidate/profile/', CandidateProfileView.as_view(), name='candidate-profile'),
    path('candidate/jobs/', CandidateJobListView.as_view(), name='candidate-jobs'),
    path('candidate/applied-jobs/', CandidateAppliedJobsView.as_view(), name='candidate-applied-jobs'),
    path('candidate/interviews/', CandidateInterviewListView.as_view(), name='candidate-interviews'),

path('recruiter/profile/', RecruiterProfileView.as_view(), name='recruiter-profile'),
    path('recruiter/jobs/', RecruiterJobListView.as_view(), name='recruiter-jobs'),
    path('recruiter/interviews/', RecruiterInterviewListView.as_view(), name='recruiter-interviews'),
]
