from rest_framework.views import APIView
from rest_framework.response import Response
from .selectors import get_nearby_providers

class NearbyProvidersAPIView(APIView):

    def get(self, request):
        lat = float(request.GET.get('lat'))
        lon = float(request.GET.get('lon'))

        providers = get_nearby_providers(lat, lon)

        data = [
            {
                "provider_id": p["provider"].id,
                "distance": p["distance"]
            }
            for p in providers
        ]

        return Response(data)
    
    
class SmartSearchAPIView(APIView):
    
    def get(self, request):
        lat = float(request.GET.get('lat'))
        lon = float(request.GET.get('lon'))

        providers = get_ranked_providers(lat, lon)

        data = [
            {
                "provider_id": p["provider"].id,
                "rating": p["provider"].rating,
                "distance": p["distance"],
                "score": p["score"]
            }
            for p in providers
        ]

        return Response(data)