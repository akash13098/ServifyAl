from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, ProviderApplication
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProviderApplicationSerializer,
    UserSerializer
)


# ===========================
# REGISTER
# ===========================

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=201)

        return Response(serializer.errors, status=400)


# ===========================
# LOGIN
# ===========================

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "role": user.role,
                "user": UserSerializer(user).data
            })

        return Response(serializer.errors, status=400)


# ===========================
# APPLY FOR PROVIDER
# ===========================

class ApplyProviderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.role != 'USER':
            return Response({"error": "Only users can apply"}, status=403)

        if ProviderApplication.objects.filter(user=request.user).exists():
            return Response({"error": "Already applied"}, status=400)

        serializer = ProviderApplicationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Application submitted"}, status=201)

        return Response(serializer.errors, status=400)


# ===========================
# ADMIN APPROVES PROVIDER
# ===========================

class ApproveProviderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):

        if request.user.role != 'ADMIN':
            return Response({"error": "Only admin allowed"}, status=403)

        try:
            app = ProviderApplication.objects.get(user__id=user_id)
        except ProviderApplication.DoesNotExist:
            return Response({"error": "No application found"}, status=404)

        app.status = 'APPROVED'
        app.save()

        user = app.user
        user.role = 'PROVIDER'
        user.save()

        return Response({"message": "Provider approved"})


# ===========================
# ADMIN REJECTS PROVIDER
# ===========================

class RejectProviderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):

        if request.user.role != 'ADMIN':
            return Response({"error": "Only admin allowed"}, status=403)

        try:
            app = ProviderApplication.objects.get(user__id=user_id)
        except ProviderApplication.DoesNotExist:
            return Response({"error": "No application found"}, status=404)

        app.status = 'REJECTED'
        app.save()

        return Response({"message": "Application rejected"})


# ===========================
# VIEW MY APPLICATION
# ===========================

class MyApplicationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            app = ProviderApplication.objects.get(user=request.user)
        except ProviderApplication.DoesNotExist:
            return Response({"message": "No application found"}, status=404)

        serializer = ProviderApplicationSerializer(app)
        return Response(serializer.data)


# ===========================
# UPDATE LOCATION
# ===========================

class UpdateLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        user.latitude = request.data.get("latitude")
        user.longitude = request.data.get("longitude")
        user.save()

        return Response({"message": "Location updated"})


# ===========================
# LIST PROVIDERS (WITH FILTER)
# ===========================

class ProviderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        service = request.GET.get("service")

        providers = User.objects.filter(role='PROVIDER')

        if service:
            providers = providers.filter(
                providerapplication__service_type__icontains=service
            )

        data = []

        for p in providers:
            app = ProviderApplication.objects.filter(user=p).first()

            data.append({
                "id": p.id,
                "name": p.name,
                "phone": p.phone,
                "service": app.service_type if app else None,
                "experience": app.experience if app else None,
                "latitude": p.latitude,
                "longitude": p.longitude,
            })

        return Response(data)


# ===========================
# PROVIDER DETAIL
# ===========================

class ProviderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:
            provider = User.objects.get(id=pk, role='PROVIDER')
        except User.DoesNotExist:
            return Response({"error": "Provider not found"}, status=404)

        app = ProviderApplication.objects.filter(user=provider).first()

        data = {
            "id": provider.id,
            "name": provider.name,
            "phone": provider.phone,
            "service": app.service_type if app else None,
            "experience": app.experience if app else None,
            "skills": app.skills if app else None,
            "latitude": provider.latitude,
            "longitude": provider.longitude,
        }

        return Response(data)


# ===========================
# UPDATE PROVIDER PROFILE
# ===========================

class UpdateProviderProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.role != 'PROVIDER':
            return Response({"error": "Only provider allowed"}, status=403)

        app = ProviderApplication.objects.filter(user=request.user).first()

        if not app:
            return Response({"error": "Application not found"}, status=404)

        app.service_type = request.data.get("service_type", app.service_type)
        app.experience = request.data.get("experience", app.experience)
        app.skills = request.data.get("skills", app.skills)

        app.save()

        return Response({"message": "Profile updated"})