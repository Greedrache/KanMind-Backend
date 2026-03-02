from django.urls import path
from .views import UserProfileList, UserProfileDetail, RegistrationView, CustomLoginView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('profiles/', UserProfileList.as_view(), name='userprofile-list'),
    path('profiles/<int:pk>/', UserProfileDetail.as_view(), name='userprofile-detail'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Endpoint for obtaining auth token
]