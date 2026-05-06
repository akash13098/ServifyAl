from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer
from .services import register_user
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from .services import login_user
from .services import send_otp_to_email
from .tasks import send_otp_email
from .services import verify_otp_and_create_user
# class RegisterAPIView(APIView):
    
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = register_user(serializer.validated_data)

#         return Response({
#             "message": "User registered successfully",
#             "user_id": user.id
#         }, status=status.HTTP_201_CREATED)
        
        
class LoginAPIView(APIView):
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = login_user(**serializer.validated_data)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })
        
class RegisterAPIView(APIView):
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pending_user, otp = register_user(serializer.validated_data)

        # send OTP email
        send_otp_email(pending_user.email, otp)

        return Response({
            "message": "OTP sent to email"
        })
        
        
class VerifyOTPAPIView(APIView):

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        verify_otp_and_create_user(email, otp)

        return Response({"message": "Account created successfully"})
    
