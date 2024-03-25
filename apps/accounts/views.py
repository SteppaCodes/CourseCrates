#django imports 
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode

#third party imports
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
#local imports
from .serializers import (RegisterSerializer, 
                          VerifyOtpSerializer, ResendOtpSerializer,
                          LoginSerializer, UserSerializer, LogoutSerializer,
                          ResetPasswordSerializer, SetNewPasswordSerializer
                          )
from .email import SendMail
from . models import OneTimePassword, User

tags = ["Auth"]

class RegisterUserView(APIView):
    serializer_class = RegisterSerializer

    @extend_schema(
            summary = "Register user",
            description="This endpoint creates a new user",
            tags=tags
    )
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            SendMail.send_otp(user['email'])
            return  Response(
                {'data': user,
                'messsage':f"Hi {user['first_name']} thank you for signing up, please check your email for an otp"}
            )


class VerifyEmail(APIView):
    serializer_class = VerifyOtpSerializer

    @extend_schema(
            summary = "Verify Email",
            description="This endpoint verifies a user's email",
            tags=tags
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_otp = serializer.data['otp']
        
        try:
            user_code_object = OneTimePassword.objects.get(code=user_otp)
            user = user_code_object.user

            if not user.is_email_verified:
                user.is_email_verified = True
                user.save()
                SendMail.welcome(user.email)

                #Serialize the user model before passing it to the response
                serialized_user = UserSerializer(user).data
                return Response(
                    {'data': serialized_user,
                   'messsage':f"Your email has been verified"}
                )
            return Response({
                'message': 'email already verified'
            })
        except OneTimePassword.DoesNotExist:
            return Response({
              'message': 'Code is invalid, please try again'
            })


class ResendEmail(APIView):
    serializer_class = ResendOtpSerializer

    @extend_schema(
            summary = "Resend verification Email",
            description="This endpoint resends verification email",
            tags=tags
    )
    def post(self, request): 
 
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            
            SendMail.send_otp(self, user.email)

            return Response(
                {
                'messsage':"Verification email sent"}
            )
        except User.DoesNotExist:
            return Response({
             'message': 'User with email does not exist'
            })


class LoginView(APIView):
    serializer_class = LoginSerializer

    @extend_schema(
            summary = "Login a user",
            description="This endpoint logs in a user",
            tags=tags
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data)


class ResetPasswordRequestView(APIView):
    serializer_class = ResetPasswordSerializer

    @extend_schema(
            summary = "Request to Reset a user's password",
            description="This endpoint sends a reset password email with link to reset password",
            tags=tags
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            SendMail.resetpassword(request, email)
            return Response({'message':'An email has been sent to you'})


class ResetPasswordConfirm(APIView):

    @extend_schema(
            summary = "Confirm passsword request",
            description="This endpoint confirms a user's password reset link",
            tags=tags
    )
    def get(self,request, uidb64, token):
        user_id = smart_str(urlsafe_base64_decode(uidb64))
        try:
            user = User.objects.get(id=user_id)
            if PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    'success':True, 'message':'credentials are valid',
                    'token':token, 'uidb64':uidb64
                })
            return Response({'message':'Token is invalid or expired'})
        
        except DjangoUnicodeDecodeError:
            return Response({'message':'User does not exist'})
        
class SetNewPassswordView(APIView):
    serializer_class = SetNewPasswordSerializer


    @extend_schema(
            summary = "Reset Password",
            description="This endpoint changes the user's password",
            tags=tags
    )
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)   

        return Response({
            'message':'Password reset successfully'
        })
    

class LogoutUserView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
            summary = "logout user",
            description="This endpoint logs out a user",
            tags=tags
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success':True,'message':"Successfully logged out"})
        

