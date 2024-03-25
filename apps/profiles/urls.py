from django.urls import path

from . views import (
    CompleteProfileView
)

urlpatterns = [
    path('complete-profile/', CompleteProfileView.as_view(), name='complete-profile'),
]