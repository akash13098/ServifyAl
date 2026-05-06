from rest_framework.views import APIView
from rest_framework.response import Response
from .selectors import get_all_categories
from .serializers import ServiceCategorySerializer

class ServiceCategoryListAPIView(APIView):

    def get(self, request):
        categories = get_all_categories()
        serializer = ServiceCategorySerializer(categories, many=True)

        return Response(serializer.data)