from django.urls import path

from . views import (
    CompleteProfileView,
    UserProfileAPIView
)

urlpatterns = [
    path('complete-profile/', CompleteProfileView.as_view(), name='complete-profile'),
    path('profiles/<slug>', UserProfileAPIView.as_view(), name="user-profile")
]