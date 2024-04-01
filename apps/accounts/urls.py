from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
                    RegisterUserView, 
                    VerifyEmail, 
                    ResendEmail, 
                    LoginView, 
                    ResetPasswordConfirm,
                    ResetPasswordRequestView, 
                    SetNewPassswordView, 
                    LogoutUserView
                )

urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('verify-email/', VerifyEmail.as_view()),
    path('resend-email/', ResendEmail.as_view()),
    path('login/', LoginView.as_view(), name="login"),
    path("logout/", LogoutUserView.as_view(),  name='logout'),
    path('reset-password-request/', ResetPasswordRequestView.as_view()),
    path('reset-password-confirm/<uidb64>/<token>/', ResetPasswordConfirm.as_view(), name='reset-password-confirm'),
    path('set-new-password/', SetNewPassswordView.as_view()),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]