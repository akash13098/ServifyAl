from django.urls import path
from .views import *

urlpatterns = [

    # ===========================
    # AUTH
    # ===========================
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),


    # ===========================
    # PROVIDER APPLICATION
    # ===========================
    path('provider/apply/', ApplyProviderView.as_view()),
    path('provider/my/', MyApplicationView.as_view()),

    path('provider/approve/<int:user_id>/', ApproveProviderView.as_view()),
    path('provider/reject/<int:user_id>/', RejectProviderView.as_view()),


    # ===========================
    # PROVIDER FEATURES
    # ===========================
    path('providers/', ProviderListView.as_view()),                 # list all providers
    path('provider/<int:pk>/', ProviderDetailView.as_view()),       # provider detail
    path('provider/update-profile/', UpdateProviderProfileView.as_view()),


    # ===========================
    # LOCATION
    # ===========================
    path('provider/update-location/', UpdateLocationView.as_view()),
]